# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import urllib

from simplejson.encoder import JSONEncoderForHTML

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, InvalidPage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.models import inlineformset_factory
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.datastructures import SortedDict

from viking.jobs.models import JobSector, Job, JobCandidate, JobAttachment, Company, Vessel, Rank
from viking.profiles.forms import RecruiterMessageForm, RecruiterNoteForm

from viking.profiles import models as profile_models

from viking.profiles.utils import profile_edit
from viking.searches.forms import SearchPreferenceForm
from viking.searches.models import SearchPreference

from .utils import form_to_dict, search_dict_list, email_user_message
from .forms import (
    JobEditForm, JobEditStatusForm, JobFilterForm, JobStatusForm, JobNoteForm,
    CandidateSearchForm, AddCandidateForm, UpdateCandidateForm,
    get_candidate_message_form, ManagedUserFilterForm, SearchForm, DashboardTimelineForm,
    RecruiterTimelineForm, CompanyEditForm, VesselEditForm
)


@permission_required('jobs.recruiter_staff')
def dashboard(request, sector=None):
    log_entries = profile_models.TimelineLogEntry.objects.select_related('user', 'job').exclude(
        Q(message_type=profile_models.TimelineLogEntry.CANDIDATE_UPDATE)
        | Q(message_type=profile_models.TimelineLogEntry.JOB_APPLICATION)
    ).filter(
        date__gte=datetime.date(2013, 10, 1)
    )

    search_qs = {}
    form = DashboardTimelineForm(request.GET or None)
    message_type_active = None

    recruiter = request.user

    if form.is_valid():
        message_type_active = form.cleaned_data['messages']

        if message_type_active:
            log_entries = log_entries.filter(message_type=message_type_active)

        # Build up the search query string for easy pagination
        search_qs = form_to_dict(form)

    search_params = urllib.urlencode(search_dict_list(search_qs))
    paginator = Paginator(log_entries, 10)

    try:
        page_obj = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404

    stage_jobs = SortedDict()
    stage_kwargs = {}

    if sector is not None:
        stage_kwargs['sector'] = sector

    for stage_num, stage_name in Job.STAGE_CHOICES[1:]:
        stage_jobs[stage_name] = Job.objects.select_related(
            'department', 'company', 'rank'
        ).filter(
            job_status='L', stage=stage_num, **stage_kwargs
        )

    return TemplateResponse(request, 'recruiter/dashboard.html', {
        'active_jobsector': sector,
        'jobsector_list': JobSector.objects.all(),
        'message_choices': DashboardTimelineForm.MESSAGE_CHOICES,
        'message_type_active': message_type_active,
        'page_obj': page_obj,
        'paginator': paginator,
        'recruiter': recruiter,
        'search_params': search_params,
        'search_qs': search_qs,
        'stage_jobs': stage_jobs,
    })


def dashboard_sector(request, sector_slug):
    sector = get_object_or_404(JobSector, slug=sector_slug)
    return dashboard(request=request, sector=sector)


@permission_required('jobs.recruiter_staff')
def job_edit(request, pk=None):
    if pk is not None:
        obj = get_object_or_404(Job, pk=pk)
    else:
        obj = None

    form = JobEditForm(request.POST or None, instance=obj)
    formset_class = inlineformset_factory(Job, JobAttachment, extra=1)
    formset = formset_class(instance=obj)

    if form.is_valid():
        obj = form.save(commit=False)
        formset = formset_class(request.POST, request.FILES, instance=obj)

        if formset.is_valid():
            obj.save()
            formset.save()

            # New job
            if pk is None:
                profile_models.NewJob.objects.create(job=obj, recruiter=request.user)

            # Keep on this page
            if '_continue' in request.POST:
                return HttpResponseRedirect(reverse('recruiter:job-update', kwargs={
                    'pk': obj.pk,
                }))

            return HttpResponseRedirect(reverse('recruiter:job-workflow', kwargs={
                'pk': obj.pk,
            }))

    return TemplateResponse(request, 'recruiter/job_form.html', {
        'form': form,
        'formset': formset,
    })


def job_create(request):
    return job_edit(request)


def job_update(request, pk):
    return job_edit(request, pk)


@permission_required('jobs.recruiter_staff')
def company_list_view(request):
    return TemplateResponse(request, 'recruiter/company_list.html', {
        'object_list': Company.objects.all(),
    })


@permission_required('jobs.recruiter_staff')
def company_edit(request, pk=None):
    if pk is not None:
        obj = get_object_or_404(Company, pk=pk)
    else:
        obj = None

    form = CompanyEditForm(request.POST or None, instance=obj)

    if form.is_valid():
        obj = form.save()

        return HttpResponseRedirect(reverse('recruiter:company-update', kwargs={
            'pk': obj.pk,
        }))

    return TemplateResponse(request, 'recruiter/company_form.html', {
        'form': form,
    })


def company_create(request):
    return company_edit(request)


def company_update(request, pk):
    return company_edit(request, pk)


@permission_required('jobs.recruiter_staff')
def vessel_list_view(request):
    return TemplateResponse(request, 'recruiter/vessel_list.html', {
        'object_list': Vessel.objects.all(),
    })


@permission_required('jobs.recruiter_staff')
def vessel_edit(request, pk=None):
    if pk is not None:
        obj = get_object_or_404(Vessel, pk=pk)
    else:
        obj = None

    form = VesselEditForm(request.POST or None, instance=obj)

    if form.is_valid():
        obj = form.save()

        return HttpResponseRedirect(reverse('recruiter:vessel-update', kwargs={
            'pk': obj.pk,
        }))

    return TemplateResponse(request, 'recruiter/vessel_form.html', {
        'form': form,
    })


def vessel_create(request):
    return vessel_edit(request)


def vessel_update(request, pk):
    return vessel_edit(request, pk)


@permission_required('jobs.recruiter_staff')
def job_recruitment_workflow(request, pk):
    obj = get_object_or_404(Job, pk=pk)
    notes = obj.jobnote_set.select_related('user').all()

    # Forms
    note_form = JobNoteForm()
    status_form = JobEditStatusForm(instance=obj)
    search_form = CandidateSearchForm()
    CandidateMessageForm = get_candidate_message_form(obj)
    candidate_message_form = CandidateMessageForm()

    # Search results
    user_model = get_user_model()
    search_results = user_model.objects.none()
    search_count = None
    user = request.user
    search_preferences = SearchPreference.objects.filter(user=user)

    if request.GET.get('action') == 'note':
        note_form = JobNoteForm(request.POST or None)

        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.job = obj
            note.user = request.user
            note.save()

            return HttpResponseRedirect(reverse('recruiter:job-workflow', kwargs={
                'pk': obj.pk,
            }))

    elif request.GET.get('action') == 'status':
        status_form = JobEditStatusForm(request.POST or None, instance=obj)

        if status_form.is_valid():
            status_form.save()

            return HttpResponseRedirect(reverse('recruiter:job-workflow', kwargs={
                'pk': obj.pk,
            }))

    elif request.GET.get('action') == 'search':
        search_form = CandidateSearchForm(request.POST or None)

        if search_form.is_valid():
            search_results = user_model.objects.filter(
                profile_started=True
            ).order_by(
                '-profile_featured', '-updated',
            )

            # Getting nationalities here as we joining than with Nationalities groups.
            nationality = request.POST.getlist('nationality')

            if 'nationality_group' in request.POST:
                nationality_group = profile_models.NationalityGroup.objects.get(
                    id=request.POST.getlist('nationality_group')[0]
                )
                countries_codes = [
                    country.iso_3166_1_a2 for country in nationality_group.countries.all()
                ]
                # Join codes with nationalities.
                nationality += countries_codes

            if nationality:
                search_results = search_results.filter(nationality__in=nationality)

            for search_field, search_value in search_form.cleaned_data.iteritems():

                # Do not do anything with nationality_group and nationality as its done above.
                if (
                        not search_value or search_field == 'nationality_group' or
                        search_field == 'nationality'
                ):
                    continue

                if search_field in CandidateSearchForm.FIELDS_ICONTAINS:
                    filter_key = '%s__icontains' % (search_field,)
                elif search_field in CandidateSearchForm.FIELDS_FUNCTION:
                    filter_key, search_value_func = CandidateSearchForm.FIELDS_FUNCTION[search_field]
                    search_value = search_value_func(search_value)
                elif search_field in CandidateSearchForm.FIELDS_IN:
                    filter_key = '%s__in' % (CandidateSearchForm.FIELDS_IN[search_field],)
                elif search_field in CandidateSearchForm.FIELDS_EXACT:
                    filter_key = '%s__exact' % (CandidateSearchForm.FIELDS_EXACT[search_field],)
                else:
                    filter_key = '%s__exact' % (search_field,)

                search_results = search_results.filter(**{
                    filter_key: search_value,
                })

            search_results = search_results.distinct()
            search_count = search_results.count()
            search_results = search_results[:200]

    elif request.GET.get('action') == 'addcandidate':
        candidate_obj = JobCandidate(job=obj)
        addcandidate_form = AddCandidateForm(request.POST or None, instance=candidate_obj)

        if addcandidate_form.is_valid():
            new_candidate = addcandidate_form.save()

            # Update the job stage automatically
            if new_candidate.stage > obj.stage:
                obj.stage = new_candidate.stage
                obj.save()

            return HttpResponseRedirect(reverse('recruiter:job-workflow', kwargs={
                'pk': obj.pk,
            }))

    elif request.GET.get('action') == 'rejectcandidate':
        candidate_user_id = request.POST['user']
        candidate_user = user_model.objects.get(id=candidate_user_id)
        candidate_user.rejected_positions.add(obj)

        return HttpResponseRedirect(reverse('recruiter:job-workflow', kwargs={
            'pk': obj.pk,
        }))

    elif request.GET.get('action') == 'message':
        candidate_message_form = CandidateMessageForm(request.POST or None)

        if candidate_message_form.is_valid():
            message = candidate_message_form.save(commit=False)
            message.job = obj
            message.save()

            for i in candidate_message_form.cleaned_data['candidates']:
                message.users.add(i.user)

            # Resave to send the message
            message.save()

            # Email the users
            for i in message.users.all():
                email_user_message(user=i, message=message.message, request=request, job=obj)

            return HttpResponseRedirect(reverse('recruiter:job-workflow', kwargs={
                'pk': obj.pk,
            }))

    # Stages 1-3
    stage_candidates = SortedDict()

    for i in range(1, 4):
        stage_name = JobCandidate.CANDIDATE_STAGE_CHOICES[i - 1][1]
        stage_candidates[stage_name] = obj.jobcandidate_set.select_related(
            'user', 'user__latest_position', 'user__latest_position__rank'
        ).filter(
            stage__gte=i
        )

    # Stage 4
    chosen_candidates = obj.jobcandidate_set.select_related(
        'user', 'user__latest_position', 'user__latest_position__rank'
    ).filter(stage=4)

    all_candidates_ids = obj.jobcandidate_set.select_related('user').values_list(
        'user_id', flat=True
    )

    # Rejects applicans which ones has been rejected for this job.
    job_applications = obj.jobapplication_set.select_related(
        'user', 'user__latest_position', 'user__latest_position__rank'
    ).all()

    return TemplateResponse(request, 'recruiter/job_recruitment_workflow.html', {
        'all_candidates_ids': all_candidates_ids,
        'candidate_message_form': candidate_message_form,
        'chosen_candidates': chosen_candidates,
        'note_form': note_form,
        'notes': notes,
        'object': obj,
        'job_applications': job_applications,
        'search_count': search_count,
        'search_form': search_form,
        'search_preference_form': SearchPreferenceForm(),
        'search_results': search_results,
        'stage_candidates': stage_candidates,
        'status_form': status_form,
        'search_preferences': search_preferences,
    })


@permission_required('jobs.recruiter_staff')
def job_workflow_candidate_update(request, pk):
    obj = get_object_or_404(JobCandidate, pk=pk)
    form = UpdateCandidateForm(request.POST, instance=obj)

    if form.is_valid():
        form.save()

        # Users profile will now be featured
        if obj.stage >= 3:
            obj.user.profile_featured = True
            obj.user.save()

        # Update the job stage automatically
        if obj.stage <= 3 and obj.stage > obj.job.stage:
            obj.job.stage = obj.stage
            obj.job.save()

        return HttpResponseRedirect(reverse('recruiter:job-workflow', kwargs={
            'pk': obj.job_id,
        }))
    else:
        return HttpResponseRedirect(reverse('recruiter:job-workflow', kwargs={
            'pk': obj.job_id,
        }))


@permission_required('jobs.recruiter_staff')
def job_workflow_candidate_finished(request, pk):
    obj = get_object_or_404(JobCandidate, pk=pk)
    obj.finished = True
    obj.save()

    return HttpResponseRedirect(reverse('recruiter:job-workflow', kwargs={
        'pk': obj.job_id,
    }))


@permission_required('jobs.recruiter_staff')
def job_workflow_candidate_readd(request, pk):
    obj = get_object_or_404(JobCandidate, pk=pk)
    obj.finished = False
    obj.save()

    return HttpResponseRedirect(reverse('recruiter:job-workflow', kwargs={
        'pk': obj.job_id,
    }))


@permission_required('jobs.recruiter_staff')
def job_workflow_candidate_delete(request, pk):
    obj = get_object_or_404(JobCandidate, pk=pk, stage=1)
    obj.delete()

    return HttpResponseRedirect(reverse('recruiter:job-workflow', kwargs={
        'pk': obj.job_id,
    }))


@permission_required('jobs.recruiter_staff')
def job_list_view(request):
    job_list = Job.objects.all()
    filter_search_qs = {}
    status_search_qs = {}

    filter_form = JobFilterForm(request.GET)
    status_form = JobStatusForm(request.GET)

    if filter_form.is_valid():
        # Filter the job list
        for k, v in filter_form.cleaned_data.iteritems():
            if v:
                filter_kwargs = {
                    '%s__in' % (k,): v,
                }
                job_list = job_list.filter(**filter_kwargs)

#        if status_form.cleaned_data['job_status']:
#            job_list = job_list.filter(job_status=status_form.cleaned_data['job_status'])

        # Build up the search query string for easy pagination
        filter_search_qs = form_to_dict(filter_form)

    if status_form.is_valid():
        # Filter the job list
        filter_status = status_form.cleaned_data['job_status']

        if filter_status == 'ALL':
            pass
        elif filter_status:
            job_list = job_list.filter(job_status=filter_status)
        else:
            job_list = job_list.filter(job_status='L')

        # Build up the search query string for easy pagination
        status_search_qs = form_to_dict(status_form)
    else:
        job_list = job_list.filter(job_status='L')

    search_qs = {}
    search_qs.update(filter_search_qs)
    search_qs.update(status_search_qs)

    filter_search_params = urllib.urlencode(search_dict_list(filter_search_qs))
    search_params = urllib.urlencode(search_dict_list(search_qs))

    paginator = Paginator(job_list, 10)

    try:
        page_obj = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page of results!")

    # Used for javascript enhancements
    department_ranks = {}

    for i in Rank.objects.select_related('rank_group').all():
        dept_id = i.rank_group.department_id

        if dept_id not in department_ranks:
            department_ranks[dept_id] = [i.id]
        else:
            department_ranks[dept_id].append(i.id)

    return TemplateResponse(request, 'recruiter/job_list.html', {
        'paginator': paginator,
        'page_obj': page_obj,
        'filter_form': filter_form,
        'search_qs': search_qs,
        'job_status_choices': Job.JOB_STATUS_CHOICES,
        'filter_search_params': filter_search_params,
        'search_params': search_params,
        'department_ranks': JSONEncoderForHTML().encode(department_ranks),
    })


@permission_required('jobs.recruiter_staff')
def user_managed_list(request):
    user_model = get_user_model()
    user_list = user_model.objects.filter(managed=True)
    search_qs = {}

    filter_form = ManagedUserFilterForm(request.GET)

    if filter_form.is_valid():
        # Filter the job list
        for k, v in filter_form.cleaned_data.iteritems():
            if v:
                filter_kwargs = {
                    '%s__in' % (k,): v,
                }
                user_list = user_list.filter(**filter_kwargs)

        # Build up the search query string for easy pagination
        search_qs = form_to_dict(filter_form)

    search_params = urllib.urlencode(search_dict_list(search_qs))

    paginator = Paginator(user_list, 10)

    try:
        page_obj = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page of results!")

    return TemplateResponse(request, 'recruiter/managed_list.html', {
        'paginator': paginator,
        'page_obj': page_obj,
        'filter_form': filter_form,
        'search_qs': search_qs,
        'search_params': search_params,
    })


@permission_required('jobs.recruiter_staff')
def search(request):
    search_model = Job
    search_st = 'Jobs'
    search_qs = {}

    form = SearchForm(request.GET or None)

    if form.is_valid():
        search_q = form.cleaned_data['q']
        search_st = form.cleaned_data['st']

        if search_st == 'Jobs':
            # Try a quick ID search
            if search_q.isdigit():
                try:
                    job = Job.objects.get(id=search_q)
                    return HttpResponseRedirect(reverse('recruiter:job-workflow', kwargs={
                        'pk': job.pk,
                    }))
                except Job.DoesNotExist:
                    pass

            object_list = search_model.objects.filter(Q(rank__name__icontains=search_q) | Q(department__name__icontains=search_q) | Q(sector__name__icontains=search_q) | Q(company__name__icontains=search_q) | Q(vessel__name__icontains=search_q))
        elif search_st == 'Candidates':
            search_model = get_user_model()
            object_list = search_model.objects.filter(profile_started=True).filter(Q(full_name__icontains=search_q) | Q(email__icontains=search_q))
        elif search_st == 'Companies':
            search_model = Company
            object_list = search_model.objects.filter(name__icontains=search_q)

        # Build up the search query string for easy pagination
        search_qs = form_to_dict(form)
    else:
        object_list = search_model.objects.none()

    search_params = urllib.urlencode(search_dict_list(search_qs))
    paginator = Paginator(object_list, 50)

    try:
        page_obj = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page of results!")

    return TemplateResponse(request, 'recruiter/search.html', {
        'paginator': paginator,
        'page_obj': page_obj,
        'form': form,
        'search_qs': search_qs,
        'search_params': search_params,
        'search_type': search_st,
    })


@permission_required('jobs.recruiter_staff')
def candidate_search(request):
    user_model = get_user_model()
    search_results = user_model.objects.none()
    search_qs = {}

    form = CandidateSearchForm(request.GET or None)

    if form.is_valid():
        search_results = user_model.objects.filter(profile_started=True)

        for search_field, search_value in form.cleaned_data.iteritems():
            if not search_value:
                continue

            if search_field in CandidateSearchForm.FIELDS_ICONTAINS:
                filter_key = '%s__icontains' % (search_field,)
            elif search_field in CandidateSearchForm.FIELDS_FUNCTION:
                filter_key, search_value_func = CandidateSearchForm.FIELDS_FUNCTION[search_field]
                search_value = search_value_func(search_value)
            elif search_field in CandidateSearchForm.FIELDS_IN:
                filter_key = '%s__in' % (CandidateSearchForm.FIELDS_IN[search_field],)
            elif search_field in CandidateSearchForm.FIELDS_EXACT:
                filter_key = '%s__exact' % (CandidateSearchForm.FIELDS_EXACT[search_field],)
            else:
                filter_key = '%s__exact' % (search_field,)

            search_results = search_results.filter(**{
                filter_key: search_value,
            })

        search_results = search_results.distinct()

        # Build up the search query string for easy pagination
        search_qs = form_to_dict(form)

    search_params = urllib.urlencode(search_dict_list(search_qs))
    paginator = Paginator(search_results, 50)

    try:
        page_obj = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page of results!")

    return TemplateResponse(request, 'recruiter/candidate_search.html', {
        'paginator': paginator,
        'page_obj': page_obj,
        'form': form,
        'search_qs': search_qs,
        'search_params': search_params,
    })


@permission_required('jobs.recruiter_staff')
def whiteboard(request):
    return TemplateResponse(request, 'recruiter/whiteboard.html', {
        'object_list': Vessel.objects.all(),
    })


def recruiter_profile_edit_home(request, pk):
    return recruiter_profile_edit(request, pk, 'profile')


def recruiter_profile_edit_home_readonly(request, pk):
    return recruiter_profile_edit(request, pk, 'profile', readonly=True)


def recruiter_profile_edit_readonly(request, pk, section):
    return recruiter_profile_edit(request, pk, section, readonly=True)


@permission_required('jobs.recruiter_staff')
def recruiter_profile_edit(request, pk, section, readonly=False):
    extra_context = None
    user = get_object_or_404(get_user_model(), pk=pk)

    if section == 'profile':
        # Recruiter messages (visible to user)
        message = profile_models.RecruiterMessage(user=user, recruiter=request.user)
        message_form = RecruiterMessageForm(instance=message)

        if request.GET.get('action') == 'message':
            message_form = RecruiterMessageForm(request.POST or None, instance=message)

            if message_form.is_valid():
                message = message_form.save()
                message_form = RecruiterMessageForm(instance=message)
                messages.success(request, 'Message added to timeline.')
                email_user_message(user=user, message=message.message, request=request)

        # Recruiter notes (only visible to recruiters)
        note = profile_models.RecruiterNote(user=user, recruiter=request.user)
        note_form = RecruiterNoteForm(instance=note)

        if request.GET.get('action') == 'note':
            note_form = RecruiterNoteForm(request.POST or None, instance=note)

            if note_form.is_valid():
                note_form.save()
                note_form = RecruiterNoteForm(instance=note)
                messages.success(request, 'Note added to timeline.')

        # Timeline filtering
        timeline_form = RecruiterTimelineForm(request.GET or None)
        active_timeline_filter = None
        log_entries_kwargs = {}
        timeline_qs = {}

        if timeline_form.is_valid():
            active_timeline_filter = timeline_form.cleaned_data['messages']

            if active_timeline_filter:
                log_entries_kwargs['message_type'] = active_timeline_filter
                timeline_qs = form_to_dict(timeline_form)

        timeline_params = urllib.urlencode(search_dict_list(timeline_qs))

        log_entries = profile_models.TimelineLogEntry.objects.prefetch_related(
            'content_object').select_related(
            'user', 'job', 'content_type').filter(
            user=user, **log_entries_kwargs)

        paginator = Paginator(log_entries, 10)

        try:
            page_obj = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404

        extra_context = {
            'note_form': note_form,
            'message_form': message_form,
            'timeline_filter_list': RecruiterTimelineForm.MESSAGE_CHOICES,
            'page_obj': page_obj,
            'timeline_params': timeline_params,
            'paginator': paginator,
            'recruiter_tabs': True,
            'section': section,
        }

    return profile_edit(
        request=request,
        section=section,
        user=user,
        template='recruiter/profile_edit.html',
        readonly=readonly,
        recruiter=True,
        extra_context=extra_context
    )

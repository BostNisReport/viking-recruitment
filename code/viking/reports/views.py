# -*- coding: utf-8 -*-

import datetime

from django.template.response import TemplateResponse
from django.contrib.auth.decorators import permission_required
from django.db.models import Count, Sum
from django.utils import timezone
from django.db import connection
from viking.auth.models import VikingUser
from viking.jobs.models import JobApplication, JobCandidate, Job

from .forms import ApplicationsReportForm, JobsReportForm
from .utils import export_csv


@permission_required('jobs.recruiter_staff')
def home(request):
    return TemplateResponse(request, 'reports/home.html', {
    })


@permission_required('jobs.recruiter_staff')
def applications_reports(request):
    form = ApplicationsReportForm(request.POST or None)

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        report_type = request.POST.get('report', '')

        # Need these in local format
        default_timezone = timezone.get_default_timezone()
        start_datetime = timezone.make_aware(datetime.datetime.combine(start_date, datetime.datetime.min.time()), default_timezone)
        end_datetime = timezone.make_aware(datetime.datetime.combine(end_date, datetime.datetime.max.time()), default_timezone)

        filter_kwargs = {
            'date__gte': start_datetime,
            'date__lte': end_datetime,
        }

        if report_type == 'department':
            return export_csv(request, 'Applications by department', start_date=start_date, end_date=end_date, fields=('Department', 'Applicants'),
                              queryset=JobApplication.objects.values('job__department__name').filter(**filter_kwargs).order_by('job__department__name').annotate(applicants=Count('job__department__name')))
        elif report_type == 'rank':
            return export_csv(request, 'Applications by rank', start_date=start_date, end_date=end_date, fields=('Group', 'Rank', 'Applicants'),
                              queryset=JobApplication.objects.values('job__rank__rank_group__name', 'job__rank__name').filter(**filter_kwargs).order_by('job__rank__rank_group__name', 'job__rank__name').annotate(applicants=Count('job__rank')))
        elif report_type == 'company':
            return export_csv(request, 'Applications by company', start_date=start_date, end_date=end_date, fields=('Company', 'Applicants'),
                              queryset=JobApplication.objects.values('job__company__name').filter(**filter_kwargs).order_by('job__company__name').annotate(applicants=Count('job__company__name')))
        elif report_type == 'vessel':
            return export_csv(request, 'Applications by vessel', start_date=start_date, end_date=end_date, fields=('Vessel', 'Applicants'),
                              queryset=JobApplication.objects.values('job__vessel__name').filter(**filter_kwargs).order_by('job__vessel__name').annotate(applicants=Count('job')))
        else:
            return export_csv(request, 'Applications by job', start_date=start_date, end_date=end_date, fields=('Job ID', 'Applicants'),
                              queryset=JobApplication.objects.values('job_id').filter(**filter_kwargs).order_by('job__id').annotate(applicants=Count('job')))

    return TemplateResponse(request, 'reports/applications.html', {
        'form': form,
    })


@permission_required('jobs.recruiter_staff')
def users_reports(request):
    if request.POST:
        report_type = request.POST.get('report', '')

        if report_type == 'nationality':
            return export_csv(request, 'Users by nationality', fields=('Nationality', 'Users'),
                              queryset=VikingUser.objects.values('nationality').order_by('nationality').annotate(candidates=Count('nationality')))
        elif report_type == 'age':
            cursor = connection.cursor()
            cursor.execute("SELECT date_part('year', age(date_of_birth)) AS age,COUNT(id) FROM viking_auth_vikinguser WHERE date_of_birth IS NOT NULL GROUP BY age ORDER BY age ASC")
            results = cursor.fetchall()
            return export_csv(request, 'Users by age', fields=('Age', 'Users'), field_order=(0, 1),
                              queryset=results)
        elif report_type == 'updated':
            cursor = connection.cursor()
            cursor.execute("SELECT ceil(EXTRACT(days from (current_timestamp-updated))/7) as updated_weeks,COUNT(id) FROM viking_auth_vikinguser WHERE updated IS NOT NULL GROUP BY updated_weeks ORDER BY updated_weeks ASC")
            results = cursor.fetchall()
            return export_csv(request, 'Users by last updated', fields=('Updated X weeks ago', 'Users'), field_order=(0, 1),
                              queryset=results)
        elif report_type == 'rank':
            return export_csv(request, 'Users by rank on latest position', fields=('Group', 'Rank', 'Users'), field_order=('latest_position__rank__rank_group__name', 'latest_position__rank__name', 'candidates'),
                              queryset=VikingUser.objects.values('latest_position__rank__rank_group__name', 'latest_position__rank__name').order_by('latest_position__rank__rank_group__name', 'latest_position__rank__name').annotate(candidates=Count('latest_position__rank')))
        elif report_type == 'coc':
            return export_csv(
                request,
                'Users by certificate of competency',
                fields=('Certificate of competency', 'Users'),
                queryset=VikingUser.objects.values(
                    'competencycertificate__certificate__name'
                ).order_by(
                    'competencycertificate__certificate__name'
                ).annotate(candidates=Count('competencycertificate'))
            )
        elif report_type == 'location':
            return export_csv(request, 'Users by location', fields=('Location', 'Users'), field_order=('current_location', 'candidates'),
                              queryset=VikingUser.objects.values('current_location').order_by('current_location').annotate(candidates=Count('current_location')))
        elif report_type == 'status':
            return export_csv(request, 'Users by status', fields=('Status', 'Users'),
                              queryset=VikingUser.objects.values('status').order_by('status').annotate(candidates=Count('status')))
        elif report_type == 'advert_reference':
            return export_csv(request, 'Users by advert reference', fields=('Advert Reference', 'Users'), field_order=('advert_reference__name', 'candidates'),
                              queryset=VikingUser.objects.values('advert_reference__name').order_by('advert_reference__name').annotate(candidates=Count('advert_reference')))
        elif report_type == 'managed_company':
            return export_csv(request, 'Users by managed company', fields=('Company', 'Users'),
                              queryset=VikingUser.objects.values('managed_company__name').order_by('managed_company__name').annotate(candidates=Count('managed_company')))

    return TemplateResponse(request, 'reports/users.html', {
    })


@permission_required('jobs.recruiter_staff')
def candidates_reports(request):
    if request.POST:
        return export_csv(request, 'Job candidates by stage', fields=('Stage', 'Users'), field_order=('stage', 'candidates'),
                          queryset=JobCandidate.objects.values('stage').order_by('stage').annotate(candidates=Count('stage')))

    return TemplateResponse(request, 'reports/candidates.html', {
    })


@permission_required('jobs.recruiter_staff')
def jobs_reports(request):
    form = JobsReportForm(request.POST or None)

    if form.is_valid():
        job_filter = form.cleaned_data['job_filter']
        filter_name = JobsReportForm.JOB_FILTER_DICT[job_filter]
        object_list = Job.objects.all()

        if job_filter:
            object_list = object_list.filter(job_status=job_filter)
        else:
            filter_name = 'All'

        if filter_name == 'Position Filled':
            fields_args = ('Jobs', 'Successful Candidates',)
            field_order_args = ('jobs', 'successful_candidates')
            annotate_kwargs = {
                'successful_candidates': Sum('successful_candidates'),
            }
        else:
            fields_args = ('Jobs',)
            field_order_args = ('jobs',)
            annotate_kwargs = {}

        report_type = request.POST.get('report', '')

        if report_type == 'sector':
            return export_csv(request, '%s jobs by sector' % (filter_name,), fields=('Sector',) + fields_args, field_order=('sector__name',) + field_order_args,
                              queryset=object_list.values('sector__name').order_by('sector__name').annotate(jobs=Count('sector'), **annotate_kwargs))
        elif report_type == 'company':
            return export_csv(request, '%s jobs by company' % (filter_name,), fields=('Company',) + fields_args, field_order=('company__name',) + field_order_args,
                              queryset=object_list.values('company__name').order_by('company__name').annotate(jobs=Count('company'), **annotate_kwargs))
        elif report_type == 'vessel':
            return export_csv(request, '%s jobs by vessel' % (filter_name,), fields=('Vessel',) + fields_args, field_order=('vessel__name',) + field_order_args,
                              queryset=object_list.values('vessel__name').order_by('vessel__name').annotate(jobs=Count('vessel'), **annotate_kwargs))
        elif report_type == 'rank':
            return export_csv(request, '%s jobs by rank' % (filter_name,), fields=('Group', 'Rank',) + fields_args, field_order=('rank__rank_group__name', 'rank__name',) + field_order_args,
                              queryset=object_list.values('rank__rank_group__name', 'rank__name').order_by('rank__rank_group__name', 'rank__name').annotate(jobs=Count('rank'), **annotate_kwargs))
        else:
            return export_csv(request, '%s jobs by status' % (filter_name,), fields=('Status',) + fields_args, field_order=('job_status',) + field_order_args,
                              queryset=object_list.values('job_status').order_by('job_status').annotate(jobs=Count('job_status'), **annotate_kwargs))

    return TemplateResponse(request, 'reports/jobs.html', {
        'form': form,
    })

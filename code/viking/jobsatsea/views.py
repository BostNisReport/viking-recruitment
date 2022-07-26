from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import resolve, reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.views.generic import RedirectView
from viking.jobs.models import Department, Job, JobApplication, JobSector

from .filters import JobFilter


JOBSATSEA_BASE_TEMPLATE = 'jobsatsea/base_jobs.html'


def jobsatsea_home(request, base_template=JOBSATSEA_BASE_TEMPLATE):
    r = resolve(request.path)

    return TemplateResponse(request, 'jobsatsea/jobs.html', {
        'jobsatsea_base_template': base_template,
        'job_sectors': JobSector.objects.all(),
        'departments': Department.objects.all(),
        'main_page': True,
        'filter': JobFilter(),
    }, current_app=r.namespace)


@never_cache
def jobsatsea_search(request, base_template=JOBSATSEA_BASE_TEMPLATE):
    r = resolve(request.path)

    search_filter = JobFilter(request.GET or None, queryset=Job.objects.select_related(
        'rank', 'sector', 'location', 'certification').filter(
        closes__gte=timezone.now(), job_status='L', jobs_at_sea=True)
    )

    if search_filter.is_bound and request.user.is_authenticated():
        applied_for = JobApplication.objects.filter(
            user=request.user, job__in=search_filter.qs).values_list('job_id', flat=True)
    else:
        applied_for = []

    return TemplateResponse(request, 'jobsatsea/job_filter.html', {
        'jobsatsea_base_template': base_template,
        'job_sectors': JobSector.objects.all(),
        'departments': Department.objects.all(),
        'applied_for': applied_for,
        'filter': search_filter,
    }, current_app=r.namespace)


def jobsatsea_list(request, sector_slug, department_slug=None, base_template=JOBSATSEA_BASE_TEMPLATE):
    r = resolve(request.path)

    sector = get_object_or_404(JobSector, slug=sector_slug)
    job_list = Job.objects.select_related('rank', 'sector', 'location', 'certification').filter(
        closes__gte=timezone.now(), job_status='L', jobs_at_sea=True, sector_id=sector.id)

    if department_slug is not None:
        # Don't allow departments if the sector doesn't allow it
        if not sector.show_subcategories:
            raise Http404("Sub-categories not visible for this job sector")

        department = get_object_or_404(Department, slug=department_slug)
        job_list = job_list.filter(department_id=department.id)
    else:
        department = None

    # Find out which of these the user has already applied for
    if request.user.is_authenticated():
        applied_for = JobApplication.objects.filter(
            user=request.user, job__in=job_list).values_list('job_id', flat=True)
    else:
        applied_for = []

    return TemplateResponse(request, 'jobsatsea/jobs.html', {
        'jobsatsea_base_template': base_template,
        'job_sectors': JobSector.objects.all(),
        'departments': Department.objects.all(),
        'active_sector': sector,
        'active_department': department,
        'job_list': job_list,
        'applied_for': applied_for,
        'filter': JobFilter(),
    }, current_app=r.namespace)


@never_cache
def jobsatsea_sector(request, sector_slug, base_template=JOBSATSEA_BASE_TEMPLATE):
    return jobsatsea_list(request, sector_slug, base_template=base_template)


@never_cache
def jobsatsea_category(request, sector_slug, department_slug, base_template=JOBSATSEA_BASE_TEMPLATE):
    return jobsatsea_list(request, sector_slug, department_slug, base_template=base_template)


@never_cache
def jobsatsea_detail(request, pk, base_template=JOBSATSEA_BASE_TEMPLATE):
    r = resolve(request.path)

    job = get_object_or_404(
        Job.objects.select_related('rank', 'sector', 'location', 'certification'),
        pk=pk, job_status='L', jobs_at_sea=True)

    # Find out if the user has already applied for this job
    if request.user.is_authenticated():
        applied_for = JobApplication.objects.filter(
            user=request.user, job=job).values_list('job_id', flat=True)
    else:
        applied_for = []

    return TemplateResponse(request, 'jobsatsea/job_detail.html', {
        'jobsatsea_base_template': base_template,
        'object': job,
        'applied_for': applied_for,
    }, current_app=r.namespace)


@require_POST
def jobsatsea_apply(request, pk, base_template=JOBSATSEA_BASE_TEMPLATE):
    r = resolve(request.path)
    job = get_object_or_404(Job, pk=pk, job_status='L', jobs_at_sea=True)

    # Redirect to a different page - as this one requires a post
    if not request.user.is_authenticated():
        detail_url = reverse('jobsatsea:job-detail', kwargs={
            'pk': job.pk,
        }, current_app=r.namespace)
        return redirect_to_login(next=detail_url)

    # Always successful to avoid a duplicate
    JobApplication.objects.get_or_create(job=job, user=request.user)

    return HttpResponseRedirect(reverse('jobsatsea:form-thanks', current_app=r.namespace))


def jobsatsea_thanks(request, base_template=JOBSATSEA_BASE_TEMPLATE):
    r = resolve(request.path)

    return TemplateResponse(request, 'jobsatsea/thanks.html', {
        'jobsatsea_base_template': base_template,
    }, current_app=r.namespace)


class JobsRedirectView(RedirectView):
    jobs_current_app = None

    def get_redirect_url(self, **kwargs):
        jobs_base_url = reverse('jobsatsea:home', current_app=self.jobs_current_app)
        return '%s%s' % (jobs_base_url, kwargs.get('jobsatsea_url'))


class ProfileJobsRedirectView(JobsRedirectView):
    jobs_current_app = 'profiles_jos'

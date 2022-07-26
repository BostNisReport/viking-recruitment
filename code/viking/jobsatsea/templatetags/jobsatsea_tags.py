from django import template
from viking.jobs.models import Job
from django.utils import timezone


register = template.Library()


@register.assignment_tag
def get_latest_jobs():
    return Job.objects.select_related('rank').filter(closes__gte=timezone.now(), job_status='L', jobs_at_sea=True).order_by('-id')[:16]

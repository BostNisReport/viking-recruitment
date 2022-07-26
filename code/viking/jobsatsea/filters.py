import django_filters
from viking.jobs.models import Job


class JobFilter(django_filters.FilterSet):
    rank = django_filters.CharFilter(name='rank__name', lookup_type='icontains', required=True)

    class Meta:
        model = Job
        fields = ('rank', 'location')

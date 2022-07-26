from django.utils import timezone

import django_filters

from rest_framework import filters, serializers
from rest_framework.reverse import reverse
from rest_framework.viewsets import ReadOnlyModelViewSet

from viking.jobs.models import Job, Rank


class RankSerializer(serializers.ModelSerializer):
    rank_group = serializers.StringRelatedField()

    class Meta:
        model = Rank
        fields = ('name', 'rank_group')


class JobSerializer(serializers.ModelSerializer):
    sector = serializers.StringRelatedField()
    department = serializers.SerializerMethodField()
    company = serializers.StringRelatedField()
    job_type = serializers.CharField(source='get_job_type_display')
    certification = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    rank = RankSerializer()
    location = serializers.StringRelatedField()
    url = serializers.SerializerMethodField('job_url')

    class Meta:
        model = Job
        fields = (
            'id', 'sector', 'company', 'job_type', 'department', 'rank', 'certification',
            'experience_required', 'created', 'currency', 'salary', 'location', 'description',
            'description_text', 'url')

    def job_url(self, obj):
        request = self.context.get('request')
        return reverse('jobsatsea:job-detail', kwargs={
            'pk': obj.pk,
        }, request=request)


class JobFilter(django_filters.FilterSet):
    sector = django_filters.CharFilter(name='sector__slug')

    class Meta:
        model = Job
        fields = ('company', 'sector')


class JobViewSet(ReadOnlyModelViewSet):
    queryset = Job.objects.select_related(
        'sector', 'department', 'company', 'rank', 'certification', 'rank__rank_group', 'location'
        ).filter(jobs_at_sea=True, job_status='L')
    serializer_class = JobSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = JobFilter

    def get_queryset(self):
        qs = super(JobViewSet, self).get_queryset()
        return qs.filter(closes__gte=timezone.now())

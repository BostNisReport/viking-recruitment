from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TimelineLogEntry


@receiver(post_save, sender='jobs.JobApplication')
def add_jobapplication(instance, raw, **kwargs):
    if raw:
        return

    TimelineLogEntry.objects.get_or_create(
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.pk,
        defaults={
            'user': instance.user,
            'job': instance.job,
            'date': instance.date,
            'message_type': TimelineLogEntry.JOB_APPLICATION,
        })

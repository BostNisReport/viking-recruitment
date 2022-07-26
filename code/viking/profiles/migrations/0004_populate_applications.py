# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


JOB_APPLICATION_ID = 102


def populate_applications(apps, schema_editor):
    JobApplication = apps.get_model('jobs', 'JobApplication')
    TimelineLogEntry = apps.get_model('profiles', 'TimelineLogEntry')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    try:
        application_type = ContentType.objects.get(
            app_label=JobApplication._meta.app_label,
            model=JobApplication._meta.model_name)
    except ContentType.DoesNotExist:
        # If the content type doesn't exist, then everything is empty anyway
        return

    for obj in JobApplication.objects.all().iterator():
        TimelineLogEntry.objects.create(
            user_id=obj.user_id,
            job_id=obj.job_id,
            date=obj.date,
            message_type=JOB_APPLICATION_ID,
            content_type_id=application_type.id,
            object_id=obj.id)


def remove_applications(apps, schema_editor):
    JobApplication = apps.get_model('jobs', 'JobApplication')
    TimelineLogEntry = apps.get_model('profiles', 'TimelineLogEntry')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    application_type = ContentType.objects.get(
        app_label=JobApplication._meta.app_label,
        model=JobApplication._meta.model_name)

    TimelineLogEntry.objects.filter(content_type_id=application_type.id).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_remove_timelinelogentry_object_repr'),
        ('jobs', '0002_initial_2'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_applications, remove_applications),
    ]

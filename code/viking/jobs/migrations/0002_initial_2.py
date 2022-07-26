# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminsortable.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='jobnote',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jobcandidate',
            name='job',
            field=models.ForeignKey(to='jobs.Job'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jobcandidate',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='jobcandidate',
            unique_together=set([('job', 'user')]),
        ),
        migrations.AddField(
            model_name='jobattachment',
            name='job',
            field=models.ForeignKey(to='jobs.Job'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='job',
            field=models.ForeignKey(to='jobs.Job'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='jobapplication',
            unique_together=set([('job', 'user')]),
        ),
        migrations.AddField(
            model_name='job',
            name='certification',
            field=models.ForeignKey(blank=True, to='jobs.CertificateOfCompetency', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='classification_society',
            field=models.ForeignKey(blank=True, to='jobs.ClassificationSociety', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='company',
            field=models.ForeignKey(to='jobs.Company'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='department',
            field=models.ForeignKey(to='jobs.Department'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='location',
            field=models.ForeignKey(blank=True, to='jobs.Location', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='rank',
            field=models.ForeignKey(blank=True, to='jobs.Rank', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='sector',
            field=models.ForeignKey(to='jobs.JobSector'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='vessel',
            field=models.ForeignKey(blank=True, to='jobs.Vessel', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='sector',
            field=models.ForeignKey(to='jobs.JobSector'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='certificateofcompetency',
            name='department',
            field=adminsortable.fields.SortableForeignKey(to='jobs.Department'),
            preserve_default=True,
        ),
    ]

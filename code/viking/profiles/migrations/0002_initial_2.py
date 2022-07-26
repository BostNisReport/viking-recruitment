# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0001_initial'),
        ('jobs', '0002_initial_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='timelinelogentry',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='statusupdate',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recruiternote',
            name='recruiter',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recruiternote',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recruitermessage',
            name='recruiter',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recruitermessage',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='previouswork',
            name='rank',
            field=models.ForeignKey(verbose_name='Position', blank=True, to='jobs.Rank', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='previouswork',
            name='trade',
            field=models.ForeignKey(blank=True, to='jobs.Trade', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='previouswork',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='previouswork',
            name='vessel_type',
            field=models.ForeignKey(blank=True, to='jobs.VesselType', help_text=b"For Hospitality roles please select 'Shore Based'", null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='othercertification',
            name='certificate',
            field=models.ForeignKey(to='jobs.OtherCertificate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='othercertification',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newjob',
            name='job',
            field=models.ForeignKey(to='jobs.Job'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newjob',
            name='recruiter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newcandidate',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nationalitygroup',
            name='countries',
            field=models.ManyToManyField(to='profiles.Country'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='marinecertification',
            name='certificate',
            field=models.ForeignKey(to='jobs.MarineCertificate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='marinecertification',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='languageproficiency',
            name='language',
            field=models.ForeignKey(to='profiles.Language'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='languageproficiency',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='languageproficiency',
            unique_together=set([('user', 'language')]),
        ),
        migrations.AddField(
            model_name='document',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='curriculumvitae',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='competencycertificate',
            name='certificate',
            field=models.ForeignKey(verbose_name='Certificate', blank=True, to='jobs.CertificateOfCompetency', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='competencycertificate',
            name='issuing_authority',
            field=models.ForeignKey(blank=True, to='profiles.Country', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='competencycertificate',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='candidatemessage',
            name='job',
            field=models.ForeignKey(to='jobs.Job'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='candidatemessage',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]

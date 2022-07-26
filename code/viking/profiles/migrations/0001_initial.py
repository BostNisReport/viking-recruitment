# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import viking.profiles.models
import django.utils.timezone
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvertReference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('published', models.BooleanField(default=True, db_index=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CandidateMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('message', models.TextField()),
            ],
            options={
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompetencyCertificate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('expiry_date', models.DateField(null=True, verbose_name='Expiry date', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('iso_3166_1_a2', models.CharField(help_text='http://en.wikipedia.org/wiki/ISO_3166-1#Current_codes', max_length=2, serialize=False, verbose_name='ISO 3166-1 alpha-2', primary_key=True)),
                ('iso_3166_1_a3', models.CharField(max_length=3, verbose_name='ISO 3166-1 alpha-3', blank=True)),
                ('iso_3166_1_numeric', models.CharField(max_length=3, verbose_name='ISO 3166-1 numeric', blank=True)),
                ('name', models.CharField(max_length=128, verbose_name='Country name')),
                ('display_order', models.PositiveSmallIntegerField(default=0, help_text='Higher the number, higher the country in the list.', verbose_name='Display order', db_index=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Countries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CurriculumVitae',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(), max_length=200, upload_to=viking.profiles.models.curriculum_vitae_path)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(), max_length=200, upload_to='profiles/document/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LanguageProficiency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('proficiency', models.PositiveSmallIntegerField(choices=[(4, '1st Language'), (3, 'Fluent'), (2, 'Intermediate'), (1, 'Basic')])),
                ('marlins_certificate', models.BooleanField(default=False, db_index=True)),
                ('marlins_certificate_expiry_date', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MarineCertification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('certificate_number', models.CharField(max_length=100, blank=True)),
                ('issue_date', models.DateField(null=True, blank=True)),
                ('expiry_date', models.DateField(null=True, blank=True)),
                ('issued_at', models.CharField(max_length=100, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('message', models.TextField()),
            ],
            options={
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NationalityGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewCandidate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
            ],
            options={
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
            ],
            options={
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OtherCertification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('certificate_number', models.CharField(max_length=100, blank=True)),
                ('issue_date', models.DateField(null=True, blank=True)),
                ('expiry_date', models.DateField(null=True, blank=True)),
                ('issued_at', models.CharField(max_length=100, blank=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PreviousWork',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('work_type', models.PositiveSmallIntegerField(blank=True, null=True, choices=[(1, 'Sea Going Job'), (2, 'Shore Based Job'), (3, 'Hospitality Job'), (4, 'Other Job')])),
                ('date_from', models.DateField(db_index=True, null=True, blank=True)),
                ('date_to', models.DateField(db_index=True, null=True, blank=True)),
                ('company', models.CharField(max_length=256, verbose_name='Company or Vessel name')),
                ('description', models.TextField(blank=True)),
                ('gross_registered_tonnage', models.CharField(max_length=100, blank=True)),
                ('permission_to_make_contact', models.CharField(blank=True, max_length=1, verbose_name='Permission to make contact', choices=[(b'Y', b'Yes'), (b'N', b'No'), (b'T', b'Not at this time')])),
                ('reason_for_leaving', models.TextField(blank=True)),
                ('date_available_for_employment', models.DateField(null=True, blank=True)),
                ('employer_name', models.CharField(max_length=64, blank=True)),
            ],
            options={
                'ordering': ('-date_from', '-date_to'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RecruiterMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('message', models.TextField()),
            ],
            options={
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RecruiterNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('note', models.TextField()),
            ],
            options={
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatusUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('status', models.CharField(max_length=1, choices=[('L', 'Looking for work & available'), ('E', 'Looking for work & still employed'), ('C', 'Not looking for work')])),
            ],
            options={
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimelineLogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('message_type', models.PositiveSmallIntegerField(db_index=True, choices=[(1, 'Candidate message'), (2, 'Profile update'), (4, 'Recruiter message'), (5, 'Status update'), (101, 'Recruiter note'), (6, 'New job'), (7, 'New candidate'), (11, 'Recruiter message'), (12, 'Recruiter group message')])),
                ('message', models.TextField(blank=True)),
                ('object_id', models.TextField(null=True, blank=True)),
                ('object_repr', models.CharField(max_length=250, blank=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
                ('job', models.ForeignKey(to='jobs.Job', null=True)),
            ],
            options={
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_rename_tables'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_block', models.ForeignKey(editable=False, to='pages.ContentBlock', null=True)),
            ],
            options={
                'verbose_name': 'contact',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveSmallIntegerField(default=1, db_index=True)),
                ('contact_list', models.ForeignKey(to='team.ContactBlock')),
            ],
            options={
                'ordering': ('position',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, db_index=True)),
                ('slug', models.SlugField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ('title',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('email', models.EmailField(max_length=75)),
                ('company_title', models.CharField(max_length=100)),
                ('company_subtitle', models.CharField(max_length=100, blank=True)),
                ('image', models.ImageField(height_field='image_height', width_field='image_width', upload_to='team/profile', blank=True)),
                ('image_height', models.PositiveIntegerField(null=True, editable=False)),
                ('image_width', models.PositiveIntegerField(null=True, editable=False)),
                ('visible_profile', models.BooleanField(default=False)),
                ('content', models.TextField(blank=True)),
                ('phone_number', models.CharField(max_length=20, blank=True)),
                ('office', models.CharField(max_length=50, blank=True)),
                ('position', models.PositiveSmallIntegerField(default=1, db_index=True)),
                ('published', models.BooleanField(default=True, db_index=True)),
                ('group', models.ForeignKey(to='team.Group')),
            ],
            options={
                'ordering': ('position', 'name'),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contactprofile',
            name='profile',
            field=models.ForeignKey(to='team.Profile'),
            preserve_default=True,
        ),
    ]

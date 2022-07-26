# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, db_index=True)),
                ('image', models.ImageField(height_field='image_height', width_field='image_width', upload_to='homepage/banner')),
                ('image_height', models.PositiveIntegerField(null=True, editable=False)),
                ('image_width', models.PositiveIntegerField(null=True, editable=False)),
                ('link', models.URLField()),
                ('coloured_link_text', models.CharField(max_length=100)),
                ('link_text', models.CharField(max_length=100, blank=True)),
                ('description', models.TextField(blank=True)),
                ('position', models.PositiveIntegerField(default=1, db_index=True)),
                ('published', models.BooleanField(default=True, db_index=True)),
            ],
            options={
                'ordering': ('position',),
            },
            bases=(models.Model,),
        ),
    ]

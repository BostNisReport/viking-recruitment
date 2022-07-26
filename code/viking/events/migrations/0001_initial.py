# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_rename_tables'),
    ]

    operations = [
        migrations.CreateModel(
            name='LatestEventsBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number_of_events', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('content_block', models.ForeignKey(editable=False, to='pages.ContentBlock', null=True)),
            ],
            options={
                'verbose_name': 'latest events',
            },
            bases=(models.Model,),
        ),
    ]

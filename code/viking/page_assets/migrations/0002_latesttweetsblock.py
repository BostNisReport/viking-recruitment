# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_contentblock_unique_position'),
        ('page_assets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LatestTweetsBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_block', models.ForeignKey(editable=False, to='pages.ContentBlock', null=True)),
            ],
            options={
                'verbose_name': 'latest tweets',
            },
            bases=(models.Model,),
        ),
    ]

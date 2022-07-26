# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_rank_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificateofcompetency',
            name='order',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jobsector',
            name='order',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='order',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rank',
            name='order',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=True,
        ),
    ]

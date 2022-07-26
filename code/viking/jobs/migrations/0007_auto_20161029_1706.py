# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_upgrade_admin-sortable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificateofcompetency',
            name='order',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jobsector',
            name='order',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='order',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rank',
            name='order',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=True,
        ),
    ]

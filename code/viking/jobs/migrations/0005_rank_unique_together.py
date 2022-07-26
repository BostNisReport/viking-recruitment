# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_fix_duplicate_ranks'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rank',
            unique_together=set([('rank_group', 'name')]),
        ),
    ]

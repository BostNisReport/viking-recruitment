# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_initial_2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timelinelogentry',
            name='object_repr',
        ),
    ]

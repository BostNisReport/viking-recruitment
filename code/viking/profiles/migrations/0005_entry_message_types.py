# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_populate_applications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelinelogentry',
            name='message_type',
            field=models.PositiveSmallIntegerField(db_index=True, choices=[(1, 'Candidate message'), (2, 'Profile update'), (4, 'Recruiter message'), (5, 'Status update'), (101, 'Recruiter note'), (6, 'New job'), (7, 'New candidate'), (11, 'Recruiter message'), (12, 'Recruiter group message'), (102, 'Job application')]),
            preserve_default=True,
        ),
    ]

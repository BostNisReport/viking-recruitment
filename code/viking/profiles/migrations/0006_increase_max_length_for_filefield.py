# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_entry_message_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(), max_length=512, upload_to='profiles/document/'),
            preserve_default=True,
        ),
    ]

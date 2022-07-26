# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viking_pages', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='footerimage',
            old_name='coloured_header',
            new_name='header',
        ),
        migrations.RenameField(
            model_name='footerimage',
            old_name='plain_header',
            new_name='subhead_text',
        ),
        migrations.AddField(
            model_name='footerimage',
            name='subhead_colour',
            field=models.CharField(default='', max_length=10, choices=[('', 'White'), ('lightblue', 'Light Blue'), ('gold', 'Gold'), ('darkblue', 'Dark Blue')], blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='footerimage',
            name='header_colour',
            field=models.CharField(max_length=10, choices=[('', 'White'), ('lightblue', 'Light Blue'), ('gold', 'Gold'), ('darkblue', 'Dark Blue')], blank=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viking_pages', '0002_header_colours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footerlink',
            name='order',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='headerlink',
            name='order',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=True,
        ),
    ]

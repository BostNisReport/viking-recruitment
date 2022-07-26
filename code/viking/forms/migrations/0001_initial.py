# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_rename_tables'),
    ]

    operations = [
        migrations.CreateModel(
            name='CadetApplicationFormBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_block', models.ForeignKey(editable=False, to='pages.ContentBlock', null=True)),
                ('success_page', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='pages.Page', null=True)),
            ],
            options={
                'verbose_name': 'cadet application form',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactFormBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recipient', models.EmailField(max_length=75)),
                ('content_block', models.ForeignKey(editable=False, to='pages.ContentBlock', null=True)),
                ('success_page', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='pages.Page', null=True)),
            ],
            options={
                'verbose_name': 'contact form',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RequestQuoteFormBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recipient', models.EmailField(max_length=75)),
                ('content_block', models.ForeignKey(editable=False, to='pages.ContentBlock', null=True)),
                ('success_page', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='pages.Page', null=True)),
            ],
            options={
                'verbose_name': 'request quote form',
            },
            bases=(models.Model,),
        ),
    ]

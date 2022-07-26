# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FooterImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, db_index=True)),
                ('image', models.ImageField(height_field='image_height', width_field='image_width', upload_to='pages/footerimage')),
                ('image_height', models.PositiveIntegerField(editable=False)),
                ('image_width', models.PositiveIntegerField(editable=False)),
                ('link', models.URLField()),
                ('header_colour', models.CharField(max_length=10, choices=[('lightblue', 'Light Blue'), ('gold', 'Gold'), ('darkblue', 'Dark Blue')])),
                ('coloured_header', models.TextField()),
                ('plain_header', models.TextField()),
                ('subheader', models.CharField(max_length=100)),
                ('position', models.PositiveSmallIntegerField(default=1, db_index=True)),
            ],
            options={
                'ordering': ('position',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FooterLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=1, editable=False, db_index=True)),
                ('title', models.CharField(max_length=100, db_index=True)),
                ('link', models.URLField()),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HeaderLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=1, editable=False, db_index=True)),
                ('title', models.CharField(max_length=100, db_index=True)),
                ('link', models.URLField()),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LargeBanner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, db_index=True)),
                ('header_colour', models.CharField(max_length=10, choices=[('red', 'Red'), ('gold', 'Gold'), ('lightblue', 'Light Blue'), ('grey', 'Grey'), ('darkblue', 'Dark Blue')])),
                ('image', models.ImageField(height_field='image_height', width_field='image_width', upload_to='pages/banner')),
                ('image_height', models.PositiveIntegerField(editable=False)),
                ('image_width', models.PositiveIntegerField(editable=False)),
                ('link', models.URLField()),
                ('content', models.TextField()),
            ],
            options={
                'ordering': ('title',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('url', models.CharField(db_index=True, max_length=100, verbose_name='URL', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='viking_pages.MenuItem', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SmallBanner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, db_index=True)),
                ('header_colour', models.CharField(max_length=10, choices=[('red', 'Red'), ('gold', 'Gold'), ('lightblue', 'Light Blue'), ('grey', 'Grey'), ('darkblue', 'Dark Blue')])),
                ('image', models.ImageField(height_field='image_height', width_field='image_width', upload_to='pages/banner')),
                ('image_height', models.PositiveIntegerField(editable=False)),
                ('image_width', models.PositiveIntegerField(editable=False)),
                ('link', models.URLField()),
                ('content', models.TextField()),
            ],
            options={
                'ordering': ('title',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]

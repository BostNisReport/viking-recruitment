# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viking_pages', '0001_initial'),
        ('pages', '0004_rename_tables'),
    ]

    operations = [
        migrations.CreateModel(
            name='LargeBannerBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('banner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='viking_pages.LargeBanner', null=True)),
                ('content_block', models.ForeignKey(editable=False, to='pages.ContentBlock', null=True)),
            ],
            options={
                'verbose_name': 'banner - large',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RelatedLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('url', models.URLField(verbose_name='URL')),
                ('position', models.PositiveSmallIntegerField(default=1, db_index=True)),
            ],
            options={
                'ordering': ('position',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RelatedLinkListBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_block', models.ForeignKey(editable=False, to='pages.ContentBlock', null=True)),
            ],
            options={
                'verbose_name': 'related links',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SmallBannerBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('banner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='viking_pages.SmallBanner', null=True)),
                ('content_block', models.ForeignKey(editable=False, to='pages.ContentBlock', null=True)),
            ],
            options={
                'verbose_name': 'banner - small',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='relatedlink',
            name='related_link_list',
            field=models.ForeignKey(to='page_assets.RelatedLinkListBlock'),
            preserve_default=True,
        ),
    ]

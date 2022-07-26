# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fix_duplicate_ranks(apps, schema_editor):
    Rank = apps.get_model('jobs', 'Rank')

    rank_dict = {}
    rank_changes = {}

    for rank in Rank.objects.select_related('rank_group').all():
        rank_key = rank.rank_group.name, rank.name

        # If there's an existing (name, group), add a future change to rank_changes
        try:
            new_id = rank_dict[rank_key]
            rank_changes[rank.id] = new_id
        except KeyError:
            rank_dict[rank_key] = rank.id

    # Go through old ranks to be removed, update foreign keys so we don't lose data
    for old_id, new_id in rank_changes.items():
        rank = Rank.objects.get(id=old_id)

        rank.job_set.update(rank_id=new_id)
        rank.previouswork_set.update(rank_id=new_id)

        # ... and remove the duplicate!
        rank.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_alter_ranks'),
        ('profiles', '0005_entry_message_types'),
    ]

    operations = [
        migrations.RunPython(fix_duplicate_ranks, lambda apps, schema_editor: None),
    ]

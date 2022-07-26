from __future__ import unicode_literals

from django import forms


class RankChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return '%s - %s' % (obj.rank_group, obj.name)


def rank_group_label(obj):
    return '%s - %s' % (obj.department, obj)

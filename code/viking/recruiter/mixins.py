# -*- coding: utf-8 -*-

from django.template.defaultfilters import title
from django.forms.forms import pretty_name


class CapitalizeLabelsMixin(object):
    def __init__(self, *args, **kwargs):
        super(CapitalizeLabelsMixin, self).__init__(*args, **kwargs)
        for key, val in self.fields.items():
            if not val.label:
                val.label = title(pretty_name(key))

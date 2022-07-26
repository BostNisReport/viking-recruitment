# -*- coding: utf-8 -*-

from django import forms


NA_CHOICE_DASH = [("", "N/A")]

NULL_BOOLEANFIELD_CHOICES = (
    (None, 'N/A',),
    (True, 'Yes',),
    (False, 'No',),
)


class EmptyLabelMixin(object):
    """ Instead of dashes empty value display N/A. """

    def __init__(self, *args, **kwargs):
        for name, field in self.base_fields.items():

            # Replace ---- empty value with N/A.
            if hasattr(field, 'empty_label'):
                field.empty_label = 'N/A'

            elif hasattr(field, 'choices'):
                field.choices = NA_CHOICE_DASH + field.choices[1:]

            # Change choices for NullBooleanField.
            if isinstance(field, forms.NullBooleanField):
                field.widget.choices = NULL_BOOLEANFIELD_CHOICES

        return super(EmptyLabelMixin, self).__init__(*args, **kwargs)


class AllFieldsRequiredMixin(object):
    """ All field should be required on form. """

    def __init__(self, *args, **kwargs):
        for name, field in self.base_fields.items():
            field.required = True
        return super(AllFieldsRequiredMixin, self).__init__(*args, **kwargs)

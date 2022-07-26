# -*- coding: utf-8 -*-

from django import forms

from .models import SearchPreference


class SearchPreferenceForm(forms.ModelForm):
    class Meta:
        model = SearchPreference
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(SearchPreferenceForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Preference name'



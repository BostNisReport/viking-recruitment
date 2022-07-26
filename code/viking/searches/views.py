# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from urlparse import parse_qs

from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse

from form_utils.templatetags.form_utils import render

from viking.recruiter.forms import CandidateSearchForm

from .forms import SearchPreferenceForm
from .models import SearchPreference


@require_POST
def save_search_preferences(request):
    """ Ajax save search preferences. """
    data = {}
    created = None
    user = request.user

    form = SearchPreferenceForm(request.POST)
    if form.is_valid():
        name = request.POST.get('name')
        search_query = request.POST.get('search_query')

        # Update existing preference if exists.
        if SearchPreference.objects.filter(name=name, user=user).exists():
            obj = SearchPreference.objects.get(name=name, user=user)
            obj.search_query = search_query
            obj.save()
            created = False
        else:
            obj = form.save(commit=False)
            obj.user = request.user
            obj.search_query = search_query
            obj.save()
            created = True
        data = {'success': True, 'id': obj.id, 'created': created}
    else:
        data = {'errors': True, 'data': form.errors}

    return HttpResponse(json.dumps(data), content_type='application/json')


@require_GET
def get_preferences(request):
    """ Ajax get preference from dropdown. """

    data = {}
    id = request.GET.get('id')

    # These fields should be passed as a list.
    do_not_edit_values = [
        'nationality', 'rank', 'nationality_group', 'gender', 'vessel_type_experience',
        'coc_certificate', 'coc_issuing_authority', 'additional_certification', 'current_location',
        'languages',
    ]

    preference = SearchPreference.objects.get(id=id)

    search_query = preference.search_query

    # Get dictionary from querystring.
    initial_data = dict(parse_qs(search_query))

    # Remove csrf middleware token from initial_data.
    if 'csrfmiddlewaretoken' in initial_data:
        initial_data.pop('csrfmiddlewaretoken')

    # Strip values from the list.
    for key, val in initial_data.items():
        if key not in do_not_edit_values:
            initial_data.update({key: val[0]})

    search_form = CandidateSearchForm(initial=initial_data)
    # Render form with formutils templatetag
    html_form = render(search_form)

    data = {'form': html_form, 'active_tab': request.GET.get('active_tab')}

    return HttpResponse(json.dumps(data), content_type='application/json')


@require_POST
def delete_preference(request):
    """ Ajax delete preference. """

    id = request.POST.get('id')
    if SearchPreference.objects.filter(id=id).exists():
        SearchPreference.objects.get(id=id).delete()
        data = {'success': True}
    else:
        data = {'success': False}
    return HttpResponse(json.dumps(data), content_type='application/json')

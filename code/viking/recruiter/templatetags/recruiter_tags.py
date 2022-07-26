# -*- coding: utf-8 -*-

from django.conf import settings
from django import template

from viking.recruiter.forms import SearchForm

register = template.Library()


@register.assignment_tag
def get_recruiter_search_form():
    return SearchForm()


@register.simple_tag
def display_replies(time_log_entry, recruiter_id):
    image = ''
    if time_log_entry.message_type == time_log_entry.MESSAGE:
        if time_log_entry.user.recruitermessage_set.filter(recruiter__id=recruiter_id):
            image = '<img src="{}admin/img/icon-yes.gif" alt="True">'.format(
                settings.STATIC_URL
            )
    return image


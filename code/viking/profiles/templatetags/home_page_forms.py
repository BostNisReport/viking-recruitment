# -*- coding: utf-8 -*-

from django import template

from viking.auth.forms import get_registration_form

register = template.Library()


@register.assignment_tag
def get_reg_form(request):
    return get_registration_form(request)


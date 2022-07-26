# -*- coding: utf-8 -*-

from django import template
from django.db.models import Model

register = template.Library()


@register.filter
def verbose_name(field_name, instance):
    if isinstance(instance, Model):
        name = instance._meta.get_field(field_name).verbose_name.title()
    return name


@register.filter
def get_form_field(field_name, form):
    return form[field_name]

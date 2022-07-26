# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django import template
from django.forms.fields import FileField, ImageField, BooleanField

from django.contrib.admin.helpers import AdminReadonlyField

from easy_thumbnails.files import get_thumbnailer

register = template.Library()


@register.filter
def link_field(field):
    """Filter to display value correcy value from forms"""

    value = ''

    # Display thumbnail for ImageField.
    if isinstance(field.field, ImageField):
        value = field.value()
        if value:
            # Check if file exists.
            try:
                value.file
            except IOError:
                pass
            else:
                thumbnail = get_thumbnailer(field.value())
                thumb = thumbnail.get_thumbnail({'size': (50, 50)})
                value = '<a href="{0}" target="_blank"><img src="{0}"/></a>'.format(
                    thumb.url
                )
    # Display full path to the FileField
    elif isinstance(field.field, FileField):
        file_field = field.value()
        if file_field.name:
            try:
                url = file_field.url
            except TypeError:
                url = '#'
            value = '<a href="{}" target="_blank">{}</a>'.format(
                url, os.path.basename(file_field.name)
            )
    elif isinstance(field.field, BooleanField) or isinstance(field.value(), bool):
        value = field.value()
        if value:
            value = 'Yes'
        else:
            value = 'No'

    else:
        value = field.value()

        # If displau 'N/A' ir value is None.
        if value is None:
            value = 'N/A'

        elif value:
            value = AdminReadonlyField(field.form, field.name, is_first=0).contents()

    return value

register.filter('link_field', link_field)

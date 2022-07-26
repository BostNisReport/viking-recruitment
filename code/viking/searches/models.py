# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class SearchPreference(models.Model):
    name = models.CharField(max_length=120)
    search_query = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.save_search_preferences, name='save-preferences'),
    url(r'^get-preference/$', views.get_preferences, name='get-preferences'),
    url(r'^delete/$', views.delete_preference, name='delete-preferences'),
)


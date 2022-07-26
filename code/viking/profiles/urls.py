# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
import views


urlpatterns = patterns(
    '',
    url(r'^dashboard/$',
        views.dashboard,
        name='dashboard'),
    url(
        r'^readonly/$',
        views.user_profile_home,
        name='profile-home'
    ),
    url(
        r'readonly/(?P<section>[-\w]+)/$',
        views.user_profile,
        name='profile'
    ),
    url(
        r'^edit/$',
        views.user_profile_edit_home,
        name='profile-edit-home'
    ),
    url(
        r'^edit/(?P<section>[-\w]+)/$',
        views.user_profile_edit,
        name='profile-edit'
    ),
)


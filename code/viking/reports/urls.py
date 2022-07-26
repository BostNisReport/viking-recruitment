# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^$',
        views.home,
        name='home'),
    url(r'^applications/$',
        views.applications_reports,
        name='applications'),
    url(r'^users/$',
        views.users_reports,
        name='users'),
    url(r'^candidates/$',
        views.candidates_reports,
        name='candidates'),
    url(r'^jobs/$',
        views.jobs_reports,
        name='jobs'),
)

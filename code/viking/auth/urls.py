# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from django.contrib.auth.urls import urlpatterns as auth_urlpatterns

from . import views

urlpatterns = patterns(
    '',
    url(r'^profile/$',
        views.profile_redirect,
        name='profile-redirect'),

    url(r'^banned/$',
        views.BannedView.as_view(),
        name='registration_banned'),

    # Registration
    url(
        r'^register/$',
        views.UserRegistrationFormView.as_view(),
        name='registration_register'
    ),

    url(
        r'^register/complete/$',
        views.RegistrationCompleteView.as_view(),
        name='registration_complete'
    ),

    # Activation
    url(r'^activate/(?P<pk>\d+)/(?P<activation_key>\w+)/$',
        views.activate,
        name='registration_activate'),
    url(r'^activate/complete/$',
        views.ActivateCompleteView.as_view(),
        name='registration_activate_complete'),
)

urlpatterns += auth_urlpatterns

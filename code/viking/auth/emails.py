# -*- coding: utf-8 -*-

from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_prompt_email_to_update_profile(user, period):
    """ Send invitation email for ticketing system. """

    email_body = render_to_string('auth/emails/prompt_update_email.txt', {
        'user': user,
        'period': period,
    })
    html_body = render_to_string('auth/emails/prompt_update_email.html', {
        'user': user,
        'period': period,
        'site': Site.objects.get_current(),
    })

    email = EmailMultiAlternatives(
        subject='Please update your profile', body=email_body, to=[user.email])
    email.attach_alternative(html_body, 'text/html')
    email.send()


def send_activation_email(request, user):
    email_body = render_to_string('registration/activation_email.txt', {
        'site': get_current_site(request),
        'protocol': request.is_secure() and 'https' or 'http',
        'new_user': user,
    })
    html_body = render_to_string('registration/activation_email.html', {
        'site': get_current_site(request),
        'protocol': request.is_secure() and 'https' or 'http',
        'new_user': user,
    })

    email = EmailMultiAlternatives(
        subject='Viking Recruitment account activation', body=email_body, to=[user.email])
    email.attach_alternative(html_body, 'text/html')
    email.send()


def send_welcome_email(request, user):
    email_body = render_to_string('registration/welcome_email.txt', {
        'site': get_current_site(request),
        'protocol': request.is_secure() and 'https' or 'http',
        'new_user': user,
    })
    html_body = render_to_string('registration/welcome_email.html', {
        'site': get_current_site(request),
        'protocol': request.is_secure() and 'https' or 'http',
        'new_user': user,
    })

    email = EmailMultiAlternatives(
        subject='Congratulations on starting your Viking CV', body=email_body, to=[user.email])
    email.attach_alternative(html_body, 'text/html')
    email.send()

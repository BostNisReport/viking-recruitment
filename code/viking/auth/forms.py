# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.cache import cache
from django.core.validators import MaxLengthValidator

from .models import VikingUser, BannedIP


class VikingUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text="Raw passwords are not stored, so there is no way to see "
                  "this user's password, but you can change the password "
                  "using <a href=\"password/\">this form</a>."
    )

    class Meta:
        model = VikingUser
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(VikingUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': "A user with that email address already exists.",
        'password_mismatch': "The two password fields didn't match.",
    }

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput, help_text="Enter the same password as above, for verification.")

    class Meta:
        model = VikingUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        # Note: Now this applies to email for VikingUser model
        email = self.cleaned_data["email"]
        try:
            VikingUser.objects.get(email=email)
        except VikingUser.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class BaseUserRegistrationForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': "A user with that email address already exists.",
    }

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    latest_position = forms.CharField(validators=[MaxLengthValidator(256)])
    website = forms.URLField(required=False)
    anti_spam = forms.CharField(required=False)

    class Meta:
        model = VikingUser
        fields = (
            'first_name', 'last_name', 'email', 'password1', 'nationality',
        )

    def __init__(self, *args, **kwargs):
        super(BaseUserRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['nationality'].required = True

    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        # Note: Now this applies to email for VikingUser model
        email = self.cleaned_data["email"]
        try:
            VikingUser.objects.get(email=email)
        except VikingUser.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_website(self):
        website = self.cleaned_data['website']

        if website:
            raise forms.ValidationError('This field should be left blank')

        return website

    def clean(self):
        cleaned_data = super(BaseUserRegistrationForm, self).clean()
        email = cleaned_data.get('email')
        anti_spam = cleaned_data.get('anti_spam')

        if email:
            if anti_spam != email[::-1]:
                raise forms.ValidationError(
                    'Anti spam error - javascript is required for registration')

        return cleaned_data

    def save(self, commit=True):
        user = super(BaseUserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        # Set a random key for account activation, disable the account
        user.create_activation_key()
        user.is_active = False

        if commit:
            user.save()
        return user


CACHE_REGISTRATION_PREFIX = 'viking.auth.registration.'
CACHE_REGISTRATION_TTL = 60
HOURLY_FAIL_LIMIT = 20


def get_registration_form(request):
    class UserRegistrationForm(BaseUserRegistrationForm):
        def clean(self):
            cleaned_data = super(UserRegistrationForm, self).clean()

            # Check for permanent bans
            try:
                BannedIP.objects.get(ip_address=request.META['REMOTE_ADDR'])
                raise forms.ValidationError('Your IP address (%s) is permanently banned from registering due to abuse. Please contact us if this was in error.' % (request.META['REMOTE_ADDR'],))
            except BannedIP.DoesNotExist:
                pass

            if cache.get('%s%s' % (CACHE_REGISTRATION_PREFIX, request.META['REMOTE_ADDR'])):
                # Add our hourly statistics
                time_now = int(time.time())
                hourly_key = '%s.hour.%d.%s' % (CACHE_REGISTRATION_PREFIX, time_now - time_now % 3600, request.META['REMOTE_ADDR'])
                hourly_count = cache.get(hourly_key)

                if hourly_count > HOURLY_FAIL_LIMIT:
                    # Ban!
                    BannedIP.objects.create(ip_address=request.META['REMOTE_ADDR'])
                elif hourly_count:
                    # Count exists, just increment it
                    cache.incr(hourly_key)
                else:
                    # Doesn't exist, start off with 1
                    cache.set(hourly_key, 1, 3600)

                raise forms.ValidationError('Another user from your IP address has registered an account in the past 60 seconds. Please wait a minute and try again.')

            return cleaned_data

        def save(self, commit=True):
            user = super(UserRegistrationForm, self).save(commit=False)

            cache.set('%s%s' % (CACHE_REGISTRATION_PREFIX, request.META['REMOTE_ADDR']), True, CACHE_REGISTRATION_TTL)

            # Save registered IP address
            user.registered_ip = request.META['REMOTE_ADDR']

            if commit:
                user.save()
            return user

    return UserRegistrationForm

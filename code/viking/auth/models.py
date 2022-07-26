# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import string

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.mail import send_mail
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

from django_countries.fields import CountryField

from viking.jobs.models import CertificateOfCompetency, Job
from viking.profiles.models import AdvertReference, StatusUpdate, PreviousWork

from . import choices as auth_choies


class VikingUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = VikingUserManager.normalize_email(email)
        user = self.model(email=email, is_staff=False, is_active=True, is_superuser=False, last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class VikingUser(AbstractBaseUser, PermissionsMixin):
    TITLE_CHOICES = (
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
        ('Dr', 'Dr'),
    )

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    MARITAL_STATUS_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married'),
    )

    CURRENCY_CHOICES = (
        ('GBP', '£'),
        ('EUR', '€'),
        ('USD', '$'),
    )

    CONTACT_EMPLOYER_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
        ('T', 'Not at this time'),
    )

    STATUS_CHOICES = StatusUpdate.STATUS_CHOICES

    REGISTER_CHOICES = (
        ('Caterer Global', 'Caterer Global'),
        ('Jobs at Sea', 'Jobs at Sea'),
        ('Numast Telegraph', 'Numast Telegraph'),
        ('Other', 'Other'),
    )

    # Standard Django fields
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    full_name = models.CharField(max_length=100, editable=False, db_index=True)
    email = models.EmailField('Email address', unique=True)
    is_staff = models.BooleanField(
        'Staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.'
    )
    is_active = models.BooleanField(
        'Active',
        default=True,
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'
    )
    date_joined = models.DateTimeField('Date joined', default=timezone.now, db_index=True)

    # Additional account fields
    activation_key = models.CharField(max_length=12, blank=True)
    profile_started = models.BooleanField(default=False, db_index=True)

    # Viking fields
    title = models.CharField(max_length=4, blank=True, choices=TITLE_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = CountryField(blank=True)
    gender = models.CharField(max_length=1, blank=True, choices=GENDER_CHOICES)
    telephone = models.CharField(max_length=50, blank=True)
    telephone_2 = models.CharField(max_length=50, blank=True)
    fax = models.CharField(max_length=50, blank=True)
    mobile = models.CharField('Telephone 2', max_length=50, blank=True)
    skype = models.CharField(max_length=50, blank=True)
    linkedin = models.CharField(max_length=110, blank=True)
    address = models.TextField(blank=True)
    current_location = CountryField(blank=True)
    marital_status = models.CharField(
        max_length=1, blank=True, choices=MARITAL_STATUS_CHOICES
    )
    driving_license = models.NullBooleanField()
    height = models.CharField(max_length=50, blank=True)
    weight = models.CharField(max_length=50, blank=True)
    smoker = models.NullBooleanField()
    tattoos = models.NullBooleanField('Tattoo(s)')
    nearest_airport_1 = models.CharField('Nearest airport', max_length=50, blank=True)
    nearest_airport_2 = models.CharField(max_length=50, blank=True)

    # Next of kin
    next_of_kin_name = models.CharField('Name', max_length=100, blank=True)
    next_of_kin_relationship = models.CharField('Relationship', max_length=100, blank=True)
    next_of_kin_address = models.TextField('Address', blank=True)
    next_of_kin_telephone = models.CharField('Telephone', max_length=100, blank=True)
    next_of_kin_mobile = models.CharField('Mobile', max_length=100, blank=True)

    # Advert reference
    advert_reference = models.ForeignKey(
        AdvertReference,
        limit_choices_to={'published': True},
        null=True,
        blank=True
    )

    # Travel
    passport = models.NullBooleanField('Passport')
    passport_issue_authority = models.CharField('Issue authority', max_length=100, blank=True)
    passport_number = models.CharField(max_length=100, blank=True)
    passport_issue_date = models.DateField('Issue date', null=True, blank=True)
    passport_expiry_date = models.DateField('Expiry date', null=True, blank=True)
    passport_issued_at = models.CharField(max_length=100, blank=True)

    us_visa_c1d = models.NullBooleanField('C1/D')
    us_visa_c1d_issue_date = models.DateField('C1/D Issue date', null=True, blank=True)
    us_visa_c1d_expiry_date = models.DateField('C1/D Expiry date', null=True, blank=True)
    us_visa_b1b2 = models.NullBooleanField('B1/B2')
    us_visa_b1b2_issue_date = models.DateField('B1/B2 Issue date', null=True, blank=True)
    us_visa_b1b2_expiry_date = models.DateField('B1/B2 Expiry date', null=True, blank=True)
    schengen_visa = models.NullBooleanField('Schengen')
    schengen_visa_issue_date = models.DateField('Schengen Issue date', null=True, blank=True)
    schengen_visa_expiry_date = models.DateField('Schengen Expiry date', null=True, blank=True)

    other_visa_details = models.TextField(blank=True)

    # Partner details
    work_with_partner = models.NullBooleanField('Want to work with partner')
    partner_name = models.CharField(max_length=100, blank=True)
    partner_email = models.EmailField(blank=True)
    partner_position = models.CharField(max_length=100, blank=True)

    # References
    additional_references = models.TextField('Additional references (2 max)', blank=True)

    # Marine Docs
    discharge_book_number = models.CharField(max_length=100, blank=True)
    discharge_book_issue_authority = models.CharField(
        'Issue authority', max_length=100, blank=True
    )
    discharge_book_issue_date = models.DateField('Issue date', null=True, blank=True)
    discharge_book_expiry_date = models.DateField('Expiry date', null=True, blank=True)

    valid_medical_certificate = models.NullBooleanField()
    seafarers_medical = CountryField('Seafarer\'s medical', blank=True)
    seafarers_medical_issue_date = models.DateField('Issue date', null=True, blank=True)
    seafarers_medical_expiry_date = models.DateField('Expiry date', null=True, blank=True)

    serious_injury = models.NullBooleanField(
        'Has any serious injury or illness occured since issue?'
    )
    serious_injury_details = models.TextField('Details', blank=True)

    # Photo
    photo = models.ImageField(
        upload_to='auth/photo/',
        max_length=200,
        blank=True,
        height_field='photo_height',
        width_field='photo_width'
    )
    photo_height = models.PositiveIntegerField(null=True, editable=False)
    photo_width = models.PositiveIntegerField(null=True, editable=False)

    # Declaration
    declaration_agree = models.BooleanField('I agree', default=False, db_index=True)
    send_email = models.BooleanField('Please send emails', default=False, db_index=True)
    personal_statement = models.TextField(blank=True, validators=[MaxLengthValidator(500)])

    # Various non-editable bits
    profile_complete = models.PositiveIntegerField(default=0)
    profile_featured = models.BooleanField(
        default=False,
        db_index=True
    )
    latest_position = models.ForeignKey(
        PreviousWork,
        null=True,
        editable=False,
        on_delete=models.SET_NULL
    )
    rejected_positions = models.ManyToManyField(
        Job,
        blank=True,
        null=True,
    )
    # Additional
    status = models.CharField(choices=STATUS_CHOICES, default='L', max_length=1, db_index=True)
    managed = models.BooleanField(default=False, db_index=True)
    managed_company = models.ForeignKey('jobs.VikingManagedCompany', null=True, blank=True)
    updated = models.DateTimeField(default=timezone.now, db_index=True)
    registered_ip = models.GenericIPAddressField(blank=True, null=True, editable=False)

    prompt_email_sent = models.BooleanField(default=False)
    prompt_email_sent_date = models.DateTimeField(blank=True, null=True)

    objects = VikingUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    class Meta:
        verbose_name = 'user'
        ordering = ('-id',)

    def save(self, *args, **kwargs):
        # Auto save full name
        full_name = u'%s %s' % (self.first_name, self.last_name)
        self.full_name = full_name.strip()

        # Rough estimate of profile completion
        fields_count = 0
        fields_complete = 0

        for i in self._meta.fields:
            if not i.editable:
                continue

            if i.name in (
                'full_name', 'status', 'managed', 'managed_company', 'id', 'password',
                'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'updated'
            ):
                continue

            fields_count += 1

            if getattr(self, i.name, None) not in (None, 0, ''):
                fields_complete += 1

        accurate_percent = float(fields_complete) / fields_count * 100
        rounded_percent = int(5 * round(float(accurate_percent) / 5))

        self.profile_complete = rounded_percent

        super(VikingUser, self).save(*args, **kwargs)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = ('%s %s' % (self.first_name, self.last_name)).strip()
        if full_name:
            return full_name
        else:
            return self.email

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def create_activation_key(self):
        self.activation_key = get_random_string(length=12, allowed_chars=string.hexdigits[:16])
        return self.activation_key


class BannedIP(models.Model):
    ip_address = models.IPAddressField('IP address', unique=True)
    added = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        verbose_name = 'Banned IP'
        ordering = ('-added',)

    def __unicode__(self):
        return self.ip_address

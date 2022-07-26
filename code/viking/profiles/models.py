# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from contentfiles.storage import PrivateStorage
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from viking.jobs.models import (
    Job, MarineCertificate, OtherCertificate, VesselType, Rank, Trade, CertificateOfCompetency
)
from . import help_texts
from . import choices as profiles_choices


private_storage = PrivateStorage()


def curriculum_vitae_path(instance, filename):
    from .utils import unique_upload_path
    return unique_upload_path(instance, filename)


class TimelineLogEntry(models.Model):
    # Public entries (user can see)
    MESSAGE = 1
    PROFILE_UPDATE = 2
    RECRUITER_MESSAGE = 4
    STATUS_UPDATE = 5
    NEW_JOB = 6
    NEW_CANDIDATE = 7
    CANDIDATE_UPDATE = 11
    RECRUITER_GROUP_MESSAGE = 12

    # Private entries (user can't see)
    RECRUITER_NOTE = 101
    JOB_APPLICATION = 102

    MESSAGE_TYPE_CHOICES = (
        (MESSAGE, 'Candidate message'),
        (PROFILE_UPDATE, 'Profile update'),
        (RECRUITER_MESSAGE, 'Recruiter message'),
        (STATUS_UPDATE, 'Status update'),
        (RECRUITER_NOTE, 'Recruiter note'),
        (NEW_JOB, 'New job'),
        (NEW_CANDIDATE, 'New candidate'),
        (CANDIDATE_UPDATE, 'Recruiter message'),  # Group message for jobs, shown on candidates profiles
        (RECRUITER_GROUP_MESSAGE, 'Recruiter group message'),  # As above, shown in recruiter dashboard
        (JOB_APPLICATION, 'Job application'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True
    )
    job = models.ForeignKey(Job, null=True)
    date = models.DateTimeField(default=timezone.now, db_index=True)
    message_type = models.PositiveSmallIntegerField(db_index=True, choices=MESSAGE_TYPE_CHOICES)
    message = models.TextField(blank=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.TextField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('-date',)

    def timeline_template(self):
        if not self.content_type:
            return None

        # Temporary whilst more log entries are being moved to their models
        if self.message_type in (self.JOB_APPLICATION,):
            return 'profiles/timeline/%s_%s.html' % self.content_type.natural_key()

        return None


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateTimeField(default=timezone.now, db_index=True)
    message = models.TextField()

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        if len(self.message) > 50:
            append_ellipsis = '...'
        else:
            append_ellipsis = ''

        return u'%s%s' % (self.message[:50], append_ellipsis)

    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)
        TimelineLogEntry.objects.create(
            user=self.user,
            date=self.date,
            message_type=TimelineLogEntry.MESSAGE,
            message=self.message,
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk
        )


class CandidateMessage(models.Model):
    job = models.ForeignKey(Job)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    date = models.DateTimeField(default=timezone.now, db_index=True)
    message = models.TextField()

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        if len(self.message) > 50:
            append_ellipsis = '...'
        else:
            append_ellipsis = ''

        return u'%s%s' % (self.message[:50], append_ellipsis)

    def save(self, *args, **kwargs):
        super(CandidateMessage, self).save(*args, **kwargs)

        # Users timelines
        for i in self.users.all():
            TimelineLogEntry.objects.create(
                user=i,
                date=self.date,
                message_type=TimelineLogEntry.CANDIDATE_UPDATE,
                message=self.message,
                content_type=ContentType.objects.get_for_model(self),
                object_id=self.pk
            )

        # Recruiter timeline
        recruiter_message = u'Sent to %d stage candidates in job #%d: %s' % (
            self.users.count(), self.job.id, self.message
        )
        TimelineLogEntry.objects.create(
            job=self.job,
            date=self.date,
            message_type=TimelineLogEntry.RECRUITER_GROUP_MESSAGE,
            message=recruiter_message,
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk
        )


class RecruiterMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateTimeField(default=timezone.now, db_index=True)
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    message = models.TextField()

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        if len(self.message) > 50:
            append_ellipsis = '...'
        else:
            append_ellipsis = ''

        return u'%s%s' % (self.message[:50], append_ellipsis)

    def save(self, *args, **kwargs):
        super(RecruiterMessage, self).save(*args, **kwargs)
        TimelineLogEntry.objects.create(
            user=self.user,
            date=self.date,
            message_type=TimelineLogEntry.RECRUITER_MESSAGE,
            message=self.message,
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk
        )


class StatusUpdate(models.Model):
    STATUS_CHOICES = (
        ('L', 'Looking for work & available'),
        ('E', 'Looking for work & still employed'),
        ('C', 'Not looking for work'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateTimeField(default=timezone.now, db_index=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1)

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        return self.get_status_display()

    def save(self, *args, **kwargs):
        super(StatusUpdate, self).save(*args, **kwargs)
        TimelineLogEntry.objects.create(user=self.user, date=self.date, message_type=TimelineLogEntry.STATUS_UPDATE, message=self.get_status_display(), content_type=ContentType.objects.get_for_model(self), object_id=self.pk)


class RecruiterNote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateTimeField(default=timezone.now, db_index=True)
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    note = models.TextField()

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        if len(self.note) > 50:
            append_ellipsis = '...'
        else:
            append_ellipsis = ''

        return u'%s%s' % (self.note[:50], append_ellipsis)

    def save(self, *args, **kwargs):
        super(RecruiterNote, self).save(*args, **kwargs)
        timeline_message = u'Note by: %s\n\n%s' % (self.recruiter.get_full_name(), self.note)
        TimelineLogEntry.objects.create(user=self.user, date=self.date, message_type=TimelineLogEntry.RECRUITER_NOTE, message=timeline_message, content_type=ContentType.objects.get_for_model(self), object_id=self.pk)


class NewJob(models.Model):
    job = models.ForeignKey('jobs.Job')
    date = models.DateTimeField(default=timezone.now, db_index=True)
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        return u'Job %d created by %s' % (self.job_id, self.recruiter.get_full_name())

    def save(self, *args, **kwargs):
        super(NewJob, self).save(*args, **kwargs)
        TimelineLogEntry.objects.create(job=self.job, date=self.date, message_type=TimelineLogEntry.NEW_JOB, message=unicode(self), content_type=ContentType.objects.get_for_model(self), object_id=self.pk)


class NewCandidate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        return u'{} <{}> created an account'.format(self.user.get_full_name(), self.user.email)

    def save(self, *args, **kwargs):
        super(NewCandidate, self).save(*args, **kwargs)
        TimelineLogEntry.objects.create(
            user=self.user,
            date=self.date,
            message_type=TimelineLogEntry.NEW_CANDIDATE,
            message=unicode(self),
            content_type=ContentType.objects.get_for_model(self), object_id=self.pk
        )


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class LanguageProficiency(models.Model):
    PROFICIENCY_CHOICES = (
        (4, '1st Language'),
        (3, 'Fluent'),
        (2, 'Intermediate'),
        (1, 'Basic'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    language = models.ForeignKey(Language)
    proficiency = models.PositiveSmallIntegerField(choices=PROFICIENCY_CHOICES)
    marlins_certificate = models.BooleanField(default=False, db_index=True)
    marlins_certificate_expiry_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = (
            ('user', 'language'),
        )

    def __unicode__(self):
        return u'%s - %s' % (unicode(self.language), self.get_proficiency_display())


class MarineCertification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    certificate = models.ForeignKey(MarineCertificate)
    certificate_number = models.CharField(max_length=100, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    issued_at = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return unicode(self.certificate)


class OtherCertification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    certificate = models.ForeignKey(OtherCertificate)
    certificate_number = models.CharField(max_length=100, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    issued_at = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.certificate)


class PreviousWork(models.Model):
    WORK_TYPE_CHOICES = (
        (1, 'Sea Going Job'),
        (2, 'Shore Based Job'),
        (3, 'Hospitality Job'),
        (4, 'Other Job'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    work_type = models.PositiveSmallIntegerField(null=True, blank=True, choices=WORK_TYPE_CHOICES)
    date_from = models.DateField(db_index=True, blank=True, null=True)
    date_to = models.DateField(db_index=True, blank=True, null=True)

    vessel_type = models.ForeignKey(
        VesselType, null=True, blank=True, help_text=help_texts.PREVIOUS_WORK['vessel_type'],
    )
    rank = models.ForeignKey(Rank, null=True, blank=True, verbose_name='Position')
    company = models.CharField(
        'Company or Vessel name', max_length=256
    )
    description = models.TextField(blank=True)
    gross_registered_tonnage = models.CharField(max_length=100, blank=True)
    trade = models.ForeignKey(Trade, null=True, blank=True)
    permission_to_make_contact = models.CharField(
        'Permission to make contact',
        max_length=1,
        choices=profiles_choices.CONTACT_EMPLOYER_CHOICES,
        blank=True
    )
    reason_for_leaving = models.TextField(blank=True)
    date_available_for_employment = models.DateField(null=True, blank=True)
    employer_name = models.CharField(blank=True, max_length=64)

    class Meta:
        ordering = ('-date_from', '-date_to')

    def __unicode__(self):
        return self.company


class Document(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    file = models.FileField(
        upload_to='profiles/document/', storage=private_storage, max_length=512
    )


class CurriculumVitae(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    file = models.FileField(
        upload_to=curriculum_vitae_path,
        storage=private_storage, max_length=200
    )

    def get_filename(self):
        return os.path.basename(self.file.name)


class AdvertReference(models.Model):
    name = models.CharField(max_length=100, unique=True)
    published = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Country(models.Model):
    """
    International Organization for Standardization (ISO) 3166-1 Country list.
    The field names are a bit awkward, but kept for backwards compatibility.
    pycountry's syntax of alpha2, alpha3, name and official_name seems sane.
    """

    iso_3166_1_a2 = models.CharField(
        'ISO 3166-1 alpha-2',
        max_length=2,
        primary_key=True,
        help_text='http://en.wikipedia.org/wiki/ISO_3166-1#Current_codes',
    )

    iso_3166_1_a3 = models.CharField('ISO 3166-1 alpha-3', max_length=3, blank=True)
    iso_3166_1_numeric = models.CharField('ISO 3166-1 numeric', blank=True, max_length=3)

    #: The commonly used name; e.g. 'United Kingdom'
    name = models.CharField('Country name', max_length=128)

    display_order = models.PositiveSmallIntegerField(
        "Display order",
        default=0,
        db_index=True,
        help_text='Higher the number, higher the country in the list.'
    )

    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ('name',)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class NationalityGroup(models.Model):
    name = models.CharField(max_length=120)
    countries = models.ManyToManyField(Country)

    def __str__(self):
        return self.name


class CompetencyCertificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    certificate = models.ForeignKey(
        CertificateOfCompetency,
        null=True,
        blank=True,
        verbose_name='Certificate'
    )
    issuing_authority = models.ForeignKey(Country, blank=True, null=True)
    expiry_date = models.DateField('Expiry date', null=True, blank=True)


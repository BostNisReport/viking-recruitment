# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.html import strip_tags
from django_countries.fields import CountryField
from adminsortable.models import Sortable
from adminsortable.fields import SortableForeignKey

from . import choices as jobs_choices


class JobSector(Sortable):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    show_subcategories = models.BooleanField(default=True, help_text='Show sub-categories on jobs at sea frontend?', db_index=True)

    class Meta(Sortable.Meta):
        pass

    def __unicode__(self):
        return self.name


class Company(models.Model):
    sector = models.ForeignKey(JobSector)
    name = models.CharField(max_length=100, db_index=True)

    class Meta:
        ordering = ('sector', 'name',)
        verbose_name_plural = 'companies'

    def __unicode__(self):
        return self.name


class VikingManagedCompany(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    class Meta:
        verbose_name_plural = 'viking managed companies'

    def __unicode__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class RankGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Rank(Sortable):
    rank_group = SortableForeignKey(RankGroup)
    name = models.CharField(max_length=100, db_index=True)

    class Meta(Sortable.Meta):
        ordering = ('rank_group', 'order')
        unique_together = (
            ('rank_group', 'name'),
        )

    def __unicode__(self):
        return self.name


class CertificateOfCompetency(Sortable):
    name = models.CharField(max_length=100, unique=True)
    department = SortableForeignKey(Department)

    class Meta:
        verbose_name_plural = 'certificates of competency'

    def __unicode__(self):
        return self.name


class Trade(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class MarineCertificate(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class OtherCertificate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    certificate_type = models.IntegerField(
        choices=jobs_choices.OTHER_CERTIFICATE_CHOICES, blank=True, null=True
    )

    class Meta:
        ordering = ('-certificate_type', 'name',)

    def __unicode__(self):
        return self.name


class Location(Sortable):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class ClassificationSociety(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'classification societies'

    def __unicode__(self):
        return self.name


class VesselType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Vessel(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    company = models.ForeignKey(Company, blank=True, null=True)
    size = models.PositiveIntegerField(null=True, blank=True, help_text='Size in metres (yachts only)')

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Job(models.Model):
    CURRENCY_CHOICES = (
        ('USD', '$'),
        ('EUR', '€'),
        ('GBP', '£'),
    )

    JOB_TYPE_CHOICES = (
        ('P', 'Permanent'),
        ('T', 'Temporary'),
    )

    JOB_STATUS_CHOICES = (
        ('L', 'Live'),
        ('C', 'Cancelled'),
        ('F', 'Position Filled'),
        ('H', 'On Hold'),
    )

    ISM_CHOICES = (
        (1, 'In place'),
        (2, 'Pending'),
        (3, 'Not in place'),
    )

    STAGE_CHOICES = (
        (None, '---'),
        (0, 'Jobs to be actioned'),
        (1, 'Selected candidates'),
        (2, 'Submitted candidates'),
        (3, 'Interview stage'),
    )

    sector = models.ForeignKey(JobSector)
    company = models.ForeignKey(Company)
    vessel = models.ForeignKey(Vessel, blank=True, null=True)

    contact_name = models.CharField(max_length=100)
    contact_telephone_1 = models.CharField(max_length=100, blank=True)
    contact_telephone_2 = models.CharField(max_length=100, blank=True)
    contact_telephone_3 = models.CharField(max_length=100, blank=True)
    contact_fax = models.CharField(max_length=100, blank=True)
    contact_email_1 = models.EmailField(blank=True)
    contact_email_2 = models.EmailField(blank=True)

    job_status = models.CharField(max_length=1, choices=JOB_STATUS_CHOICES, default='L', db_index=True)
    stage = models.PositiveSmallIntegerField(choices=STAGE_CHOICES, default=0, null=True, blank=True, db_index=True)
    job_type = models.CharField(max_length=1, choices=JOB_TYPE_CHOICES, default='P')
    department = models.ForeignKey(Department)
    rank = models.ForeignKey(Rank, blank=True, null=True)
    certification = models.ForeignKey(CertificateOfCompetency, null=True, blank=True)
    experience_required = models.CharField(max_length=250, blank=True)
    jobs_at_sea = models.BooleanField(default=False, db_index=True)
    standard_terms_of_business = models.BooleanField(default=True)
    bespoke_terms_of_business = models.BooleanField(default=False)
    ism = models.PositiveSmallIntegerField('ISM', choices=ISM_CHOICES)
    classification_society = models.ForeignKey(ClassificationSociety, blank=True, null=True)
    flag = CountryField(blank=True)
    created = models.DateTimeField(default=timezone.now)
    required_by = models.DateTimeField(default=timezone.now)
    closes = models.DateTimeField(default=timezone.now)
    positions_available = models.PositiveSmallIntegerField(default=1)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    salary = models.PositiveIntegerField()
    paid_on_leave = models.BooleanField(default=False)
    length_of_visit = models.CharField(max_length=200, blank=True)

    location = models.ForeignKey(Location, null=True, blank=True)
    description = models.TextField(blank=True)
    description_text = models.TextField(editable=False)

    # Hidden fields
    successful_candidates = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        ordering = ('-id',)
        permissions = (
            ('recruiter_staff', 'Recruiter staff'),
        )

    def __unicode__(self):
        return u'Job %d' % (self.id,)

    def save(self, *args, **kwargs):
        self.description_text = strip_tags(self.description).strip()
        super(Job, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('jobsatsea:job-detail', (), {
            'pk': self.pk,
        })

    def stage_candidates(self):
        if self.stage:
            return self.jobcandidate_set.filter(stage=self.stage)
        else:
            return self.jobcandidate_set.none()


class JobAttachment(models.Model):
    job = models.ForeignKey(Job)
    file = models.FileField(upload_to='jobs/attachment')

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return u'Attachment'


class JobNote(models.Model):
    job = models.ForeignKey(Job)
    date = models.DateTimeField(default=timezone.now, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    message = models.TextField()

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        return u'Note'


class JobApplicationManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super(JobApplicationManager, self).get_queryset().select_related('job__rank', 'user')


class JobApplication(models.Model):
    job = models.ForeignKey(Job)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateTimeField(default=timezone.now, db_index=True)

    objects = JobApplicationManager()

    class Meta:
        ordering = ('-date',)
        unique_together = (
            ('job', 'user'),
        )

    def __unicode__(self):
        return unicode(self.user)


class JobCandidate(models.Model):
    CANDIDATE_STAGE_CHOICES = (
        (1, 'Selected'),
        (2, 'Submitted'),
        (3, 'Interview'),
        (4, 'Successful'),
    )

    job = models.ForeignKey(Job)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    stage = models.PositiveSmallIntegerField(choices=CANDIDATE_STAGE_CHOICES, default=1, db_index=True)
    finished = models.BooleanField(default=False)

    class Meta:
        ordering = ('user',)
        unique_together = (
            ('job', 'user'),
        )

    def __unicode__(self):
        return u'%s - stage %d' % (self.user, self.stage)

    @property
    def next_stage(self):
        return self.stage + 1

    @property
    def prev_stage(self):
        return self.stage - 1

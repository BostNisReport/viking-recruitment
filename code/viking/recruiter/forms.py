# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils import formats

from form_utils.forms import BetterForm, BetterModelForm
from django_countries import countries

from viking.auth.models import VikingUser
from viking.jobs.models import (
    Job, JobSector, Department, Rank, JobNote, JobCandidate, VesselType, CertificateOfCompetency,
    OtherCertificate, Company, Vessel, MarineCertificate
)
from viking.profiles.models import (
    CandidateMessage, TimelineLogEntry, Language, PreviousWork, NationalityGroup
)

from .mixins import CapitalizeLabelsMixin
from .utils import age_to_date


class CustomSplitDateTimeWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (forms.widgets.DateInput(attrs={'class': 'datepicker'}, format=date_format),
                   forms.widgets.TimeInput(attrs=attrs, format=time_format))
        super(CustomSplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            value = forms.util.to_current_timezone(value)
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]


class JobEditForm(BetterModelForm):
    class Meta:
        model = Job
        fieldsets = (
            ('Client', {
                'fields': ('sector', 'company', 'vessel'),
            }),
            ('Contact Details', {
                'fields': (
                    'contact_name', 'contact_telephone_1', 'contact_telephone_2',
                    'contact_telephone_3', 'contact_fax', 'contact_email_1', 'contact_email_2'
                ),
            }),
            ('Job Workflow', {
                'fields': ('stage',),
            }),
            ('Job Details', {
                'fields': (
                    'created', 'required_by', 'closes', 'job_status', 'job_type', 'department',
                    'rank', 'certification', 'experience_required', 'positions_available',
                    'currency', 'salary', 'paid_on_leave', 'length_of_visit', 'location',
                    'ism', 'flag', 'classification_society', 'standard_terms_of_business',
                    'bespoke_terms_of_business', 'jobs_at_sea', 'description'),
            }),
        )
        widgets = {
            'created': CustomSplitDateTimeWidget,
            'required_by': CustomSplitDateTimeWidget,
            'closes': CustomSplitDateTimeWidget,
        }


class JobEditStatusForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('job_status',)


class CompanyEditForm(BetterModelForm):
    class Meta:
        model = Company
        fields = ('sector', 'name')


class VesselEditForm(BetterModelForm):
    class Meta:
        model = Vessel
        fields = ('name', 'company', 'size')


class RankMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return u'%s - %s' % (obj.rank_group, obj.name)


class MarineCertificateMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return u'{}'.format(obj.name)


class AdditionalMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return u'%s - %s' % (obj.get_certificate_type_display(), obj.name)


class JobFilterForm(forms.Form):
    sector = forms.ModelMultipleChoiceField(
        queryset=JobSector.objects.all(), required=False, widget=forms.CheckboxSelectMultiple
    )
    department = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(), required=False, widget=forms.CheckboxSelectMultiple
    )
    rank = RankMultipleChoiceField(
        queryset=Rank.objects.select_related().all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )


class JobStatusForm(forms.Form):
    job_status = forms.ChoiceField(choices=Job.JOB_STATUS_CHOICES + (('ALL', 'All'),), required=False)


class JobNoteForm(forms.ModelForm):
    class Meta:
        model = JobNote
        fields = ('message',)


def rank_group_label(obj):
    return u'%s - %s' % (obj.department, obj)


class CandidateSearchForm(CapitalizeLabelsMixin, BetterForm):
    FIELDS_ICONTAINS = ('first_name', 'last_name', 'email')
    FIELDS_FUNCTION = {
        'min_age': ('date_of_birth__lte', age_to_date),
        'max_age': ('date_of_birth__gte', age_to_date),
    }
    FIELDS_IN = {
        'nationality': 'nationality',
        'rank': 'previouswork__rank',
        'gender': 'gender',
        'vessel_type_experience': 'previouswork__vessel_type',
        'coc_certificate': 'competencycertificate__certificate',
        'coc_issuing_authority': 'competencycertificate__issuing_authority',
        'additional_certification': 'othercertification__certificate',
        'marine_certificate': 'marinecertification__certificate',
        'current_location': 'current_location',
        'languages': 'languageproficiency__language',
    }
    FIELDS_EXACT = {
        'sector': 'previouswork__work_type',
    }
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    min_age = forms.IntegerField(min_value=0, required=False)
    max_age = forms.IntegerField(min_value=0, required=False)
    nationality = forms.MultipleChoiceField(choices=countries, required=False)
    nationality_group = forms.ModelMultipleChoiceField(
        queryset=NationalityGroup.objects.all(),
        required=False
    )
    gender = forms.MultipleChoiceField(
        VikingUser.GENDER_CHOICES,
        required=False
    )

    rank = RankMultipleChoiceField(
        queryset=Rank.objects.select_related().all(),
        required=False,
    )

    vessel_type_experience = forms.ModelMultipleChoiceField(
        label='Vessel Type',
        queryset=VesselType.objects.all(),
        required=False
    )

    coc_certificate = forms.ModelMultipleChoiceField(
        label='Certificates of Competency',
        queryset=CertificateOfCompetency.objects.all(),
        required=False
    )
    coc_issuing_authority = forms.MultipleChoiceField(
        label='Issuing Authority',
        choices=countries,
        required=False
    )
    marine_certificate = MarineCertificateMultipleChoiceField(
        label='Marine Certification', queryset=MarineCertificate.objects.all(), required=False
    )
    additional_certification = AdditionalMultipleChoiceField(
        label='Educational Certificates', queryset=OtherCertificate.objects.all(), required=False
    )

    us_visa_c1d = forms.BooleanField(label='C1/D', required=False)
    us_visa_b1b2 = forms.BooleanField(label='B1/B2', required=False)
    schengen_visa = forms.BooleanField(label='Schengen', required=False)
    current_location = forms.MultipleChoiceField(
        choices=countries,
        required=False
    )
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        required=False
    )

    status = forms.ChoiceField(
        choices=(('', '---------'),) + VikingUser.STATUS_CHOICES, required=False
    )
    sector = forms.ChoiceField(
        choices=(('', '---------'),) + PreviousWork.WORK_TYPE_CHOICES, required=False
    )
    vessel_type = forms.ModelChoiceField(
        queryset=VesselType.objects.all(), required=False
    )
    work_with_partner = forms.BooleanField(required=False)

    class Meta:
        fieldsets = (
            ('General', {
                'fields': (
                    'first_name', 'last_name', 'email', 'min_age', 'max_age', 'nationality',
                    'nationality_group', 'gender'
                ),
            }),
            ('Employment', {
                'fields': (
                    'rank', 'vessel_type_experience', 'status', 'sector', 'work_with_partner'
                ),
            }),
            ('Education and Certification', {
                'fields': (
                    'coc_certificate', 'coc_issuing_authority', 'marine_certificate',
                    'additional_certification',
                ),
            }),
            ('Travel', {
                'fields': (
                    'us_visa_c1d', 'us_visa_b1b2', 'schengen_visa', 'current_location', 'languages'
                ),
            }),
        )


class AddCandidateForm(forms.ModelForm):
    class Meta:
        model = JobCandidate
        fields = ('user',)


class UpdateCandidateForm(forms.ModelForm):
    class Meta:
        model = JobCandidate
        fields = ('stage',)


class BaseCandidateMessageForm(BetterModelForm):
    class Meta:
        model = CandidateMessage


class StageCandidateMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        finished = ' (dropped)' if obj.finished else ''
        return u'%s%s -- %s' % (obj.get_stage_display(), finished, obj.user.get_full_name(),)


def get_candidate_message_form(job):
    class CandidateMessageForm(BaseCandidateMessageForm):
        class Meta(BaseCandidateMessageForm.Meta):
            fields = ('candidates', 'message',)

        candidates = StageCandidateMultipleChoiceField(queryset=JobCandidate.objects.select_related('user').filter(job=job).order_by('-stage'), widget=forms.widgets.CheckboxSelectMultiple)

    return CandidateMessageForm


class ManagedUserFilterForm(forms.Form):
    sector = forms.ModelMultipleChoiceField(queryset=JobSector.objects.all(), required=False)
    department = forms.ModelMultipleChoiceField(queryset=Department.objects.all(), required=False)


class SearchForm(forms.Form):
    SEARCH_CHOICES = (
        ('Jobs', 'Jobs'),
        ('Candidates', 'Candidates'),
        ('Companies', 'Companies'),
    )

    q = forms.CharField(max_length=100)
    st = forms.ChoiceField(choices=SEARCH_CHOICES)


class DashboardTimelineForm(forms.Form):
    MESSAGE_CHOICES = (
        (TimelineLogEntry.MESSAGE, 'Candidate message'),
        (TimelineLogEntry.PROFILE_UPDATE, 'Profile update'),
        (TimelineLogEntry.NEW_CANDIDATE, 'New candidate'),
        (TimelineLogEntry.NEW_JOB, 'New job'),
    )

    messages = forms.ChoiceField(choices=MESSAGE_CHOICES, required=False)


class RecruiterTimelineForm(forms.Form):
    MESSAGE_CHOICES = (
        (TimelineLogEntry.PROFILE_UPDATE, 'Profile update'),
        (TimelineLogEntry.MESSAGE, 'Message'),
        (TimelineLogEntry.RECRUITER_MESSAGE, 'Recruiter message'),
        (TimelineLogEntry.RECRUITER_NOTE, 'Note'),
        (TimelineLogEntry.JOB_APPLICATION, 'Job Application'),
    )

    messages = forms.ChoiceField(choices=MESSAGE_CHOICES, required=False)

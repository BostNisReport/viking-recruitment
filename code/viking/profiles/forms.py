# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import BaseInlineFormSet

from form_utils.forms import BetterModelForm

from viking.auth.models import VikingUser
from viking.jobs.forms import GroupedModelChoiceField
from viking.jobs.models import Rank
from .models import (
    Message, LanguageProficiency, RecruiterMessage, PreviousWork, RecruiterNote,
    MarineCertification, OtherCertification, Trade, Country, CompetencyCertificate,
    CurriculumVitae
)

from . import choices as profiles_choices
from .mixins import NA_CHOICE_DASH, AllFieldsRequiredMixin

YES_NO_SELECT = forms.Select(choices=(
    (True, 'Yes'),
    (False, 'No'),
))


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('message',)


class RecruiterMessageForm(forms.ModelForm):
    class Meta:
        model = RecruiterMessage
        fields = ('message',)


class RecruiterNoteForm(forms.ModelForm):
    class Meta:
        model = RecruiterNote
        fields = ('note',)


class ProfileBasicForm(AllFieldsRequiredMixin, BetterModelForm):
    class Meta:
        model = VikingUser
        fieldsets = (
            ('Your details', {
                'fields': ('title', 'first_name', 'last_name', 'email'),
            }),
        )


class ProfileGeneralForm(AllFieldsRequiredMixin, BetterModelForm):
    smoker = forms.ChoiceField(choices=profiles_choices.BOOLEAN_CHOICES)
    tattoos = forms.ChoiceField(choices=profiles_choices.BOOLEAN_CHOICES)

    class Meta:
        model = VikingUser
        fieldsets = (
            ('General Information', {
                'fields': (
                    'date_of_birth', 'nationality', 'gender', 'telephone', 'skype',
                    'linkedin', 'address', 'current_location', 'marital_status', 'height',
                    'weight', 'smoker', 'tattoos', 'nearest_airport_1',
                ),
            }),
        )
        widgets = {
            'date_of_birth': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
        }

    def __init__(self, *args, **kwargs):
        self.base_fields['nationality'].required = True
        self.base_fields['telephone'].required = True
        super(ProfileGeneralForm, self).__init__(*args, **kwargs)


class LanguageProficiencyForm(BetterModelForm):
    class Meta:
        model = LanguageProficiency
        fieldsets = (
            (None, {
                'fields': ('language', 'proficiency'),
            }),
            ('Certificate', {
                'fields': ('marlins_certificate', 'marlins_certificate_expiry_date'),
                'description': (
                    'A Marlins English test certificate is only required for sea going jobs'),
            }),
        )
        widgets = {
            'marlins_certificate': YES_NO_SELECT,
            'marlins_certificate_expiry_date': forms.widgets.DateInput(
                attrs={'class': 'datepicker'}),
        }


class ProfileTravelForm(BetterModelForm):

    class Meta:
        model = VikingUser
        fieldsets = (
            ('Passport', {
                'fields': (
                    'passport', 'passport_issue_authority', 'passport_expiry_date',
                ),
            }),
            ('C1/D Visa', {
                'fields': ('us_visa_c1d', 'us_visa_c1d_issue_date', 'us_visa_c1d_expiry_date'),
                'description': 'A C1/D US Visa is only required for sea going jobs',
            }),
            ('B1/B2 Visa', {
                'fields': ('us_visa_b1b2', 'us_visa_b1b2_issue_date', 'us_visa_b1b2_expiry_date'),
                'description': 'A B1/B2 US Visa is only required for sea going jobs',
            }),
            ('Schengen Visa', {
                'fields': (
                    'schengen_visa', 'schengen_visa_issue_date', 'schengen_visa_expiry_date'),
            }),
            ('Other Visa(s)', {
                'fields': ('other_visa_details',),
            }),
            ('Discharge Book/Seamans Book', {
                'fields': (
                    'discharge_book_number', 'discharge_book_issue_authority',
                    'discharge_book_issue_date', 'discharge_book_expiry_date'
                ),
                'description': (
                    'A Discharge book or Seamans book is only required for sea going jobs'),
            }),
        )
        widgets = {
            'passport_issue_date': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
            'passport_expiry_date': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
            'us_visa_c1d_issue_date': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
            'us_visa_c1d_expiry_date': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
            'us_visa_b1b2_issue_date': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
            'us_visa_b1b2_expiry_date': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
            'schengen_visa_issue_date': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
            'schengen_visa_expiry_date': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
            'discharge_book_issue_date': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
            'discharge_book_expiry_date': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
        }

    passport_issue_authority = forms.ChoiceField(choices=(), required=False)
    discharge_book_issue_authority = forms.ChoiceField(choices=(), required=False)

    def __init__(self, *args, **kwargs):
        self.base_fields['passport_issue_authority'].choices = NA_CHOICE_DASH + list(
            Country.objects.all().values_list('name', 'name',)
        )
        self.base_fields['discharge_book_issue_authority'].choices = NA_CHOICE_DASH + list(
            Country.objects.all().values_list('name', 'name',)
        )
        super(ProfileTravelForm, self).__init__(*args, **kwargs)


class ProfilePartnerReferencesForm(BetterModelForm):
    class Meta:
        model = VikingUser
        fieldsets = (
            ("Partner's Details (if applicable)", {
                'fields': (
                    'work_with_partner', 'partner_name', 'partner_email', 'partner_position'
                ),
            }),
        )
        widgets = {
            'date_available_for_employment': forms.widgets.DateInput(
                attrs={'class': 'datepicker'}
            ),
        }

    partner_position = forms.ChoiceField(choices=(), required=False)

    def __init__(self, *args, **kwargs):
        self.base_fields['partner_position'].choices = NA_CHOICE_DASH + list(
            Rank.objects.all().values_list('name', 'name'))
        super(ProfilePartnerReferencesForm, self).__init__(*args, **kwargs)


class ProfileMedicalForm(BetterModelForm):
    class Meta:
        model = VikingUser
        fieldsets = (
            ('Medical Details', {
                'fields': (
                    'valid_medical_certificate', 'seafarers_medical',
                    'seafarers_medical_issue_date', 'seafarers_medical_expiry_date'),
                'description': "A Seafarer's medical is only required for sea going jobs",
            }),
        )
        widgets = {
            'seafarers_medical_issue_date': forms.widgets.DateInput(
                attrs={'class': 'datepicker'}
            ),
            'seafarers_medical_expiry_date': forms.widgets.DateInput(
                attrs={'class': 'datepicker'}
            ),
        }
        help_texts = {
            'seafarers_medical': "A Seafarer's medical is only required for sea going jobs",
        }


def rank_group_label(obj):
    return u'%s - %s' % (obj.department, obj)


class RequiredFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)

        # At lest one form is required.
        if not self.queryset:
            for form in self.forms:
                form.empty_permitted = False


class CurriculumVitaeForm(forms.ModelForm):
    class Meta:
        model = CurriculumVitae
        exclude = ()


class PreviousWorkForm(AllFieldsRequiredMixin, BetterModelForm):
    rank = GroupedModelChoiceField(
        label='Position',
        queryset=Rank.objects.select_related().all(),
        group_by_field='rank_group',
        group_label=rank_group_label
    )
    trade = forms.ModelChoiceField(label='Location', queryset=Trade.objects.all(), required=False)

    class Meta:
        model = PreviousWork
        fieldsets = (
            (None, {
                'fields': (
                    'work_type', 'rank', 'company', 'vessel_type', 'trade', 'date_from',
                    'date_to', 'employer_name', 'permission_to_make_contact',
                    'reason_for_leaving', 'date_available_for_employment',
                ),
            }),
        )
        widgets = {
            'date_from': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
            'date_to': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
            'date_available_for_employment': forms.widgets.DateInput(
                attrs={'class': 'datepicker'}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.base_fields['date_from'].required = True
        self.base_fields['date_to'].required = True
        super(PreviousWorkForm, self).__init__(*args, **kwargs)


class ProfilePhotoForm(AllFieldsRequiredMixin, BetterModelForm):
    class Meta:
        model = VikingUser
        fieldsets = (
            ('Photograph', {
                'fields': ('photo',),
            }),
        )


class ProfileStatusForm(forms.ModelForm):
    class Meta:
        model = VikingUser
        fields = ('status',)


class ProfileDeclarationForm(BetterModelForm):
    class Meta:
        model = VikingUser
        fieldsets = (
            ('Declaration', {
                'fields': ('declaration_agree',),
                'description': (
                    'I confirm that the details given within this application are to the best of '
                    'my knowledge, accurate and true, and that I am legally in possession of any '
                    'stated qualifications and certificates. The provision of untrue information '
                    'may jeopardise employment gained and/or future assignment possibilities.'
                )
            }),
            ('Email', {
                'fields': ('send_email',),
                'description': (
                    'Please send promotional material to me advising of any news, '
                    'events, recruitment days and new services that Viking and its Family '
                    'of Companies is providing.'
                )
            }),
            ('Advert Reference', {
                'fields': ('advert_reference',),
            }),
            ('Personal statement', {
                'fields': ('personal_statement',),
                'description': (
                    'Please give details of anything else that you think may help your '
                    'application (max 500 characters).'
                )
            }),
        )


class ProfileRecruiterAdminForm(forms.ModelForm):
    class Meta:
        model = VikingUser
        fields = ('managed', 'managed_company')


class MarineCertificationForm(BetterModelForm):
    class Meta:
        model = MarineCertification
        fields = ('certificate', 'issue_date', 'expiry_date',)
        widgets = {
            'issue_date': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
            'expiry_date': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
        }


class CompetencyCertificationForm(BetterModelForm):
    class Meta:
        model = CompetencyCertificate
        fields = (
            'certificate', 'issuing_authority', 'expiry_date',
        )
        widgets = {
            'issue_date': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
            'expiry_date': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
        }


class OtherCertificationForm(BetterModelForm):
    class Meta:
        model = OtherCertification
        fields = ('certificate', 'issue_date', 'expiry_date',)
        widgets = {
            'issue_date': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
            'expiry_date': forms.widgets.DateInput(attrs={'class': 'datepicker'}),
        }

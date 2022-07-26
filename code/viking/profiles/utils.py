# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import copy

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.datastructures import SortedDict
from django.utils.text import get_text_list

from .models import (
    TimelineLogEntry, LanguageProficiency, MarineCertification, OtherCertification, PreviousWork,
    Document, NewCandidate, CompetencyCertificate, CurriculumVitae
)

from .forms import (
    ProfileBasicForm, ProfileGeneralForm, LanguageProficiencyForm, ProfileTravelForm,
    ProfilePartnerReferencesForm, ProfileMedicalForm, PreviousWorkForm, ProfilePhotoForm,
    ProfileStatusForm, ProfileDeclarationForm, ProfileRecruiterAdminForm, MarineCertificationForm,
    CompetencyCertificationForm, OtherCertificationForm, RequiredFormSet, CurriculumVitaeForm
)


EDIT_FORMS = SortedDict([
    ('profile', {
        'name': 'Profile',
        'profile_detail': True,
    }),
    ('basic', {
        'name': 'Basic Information',
        'form': ProfileBasicForm,
        'relevant_warning': False,
        'primary_fields_required': True,
        'group': {
            'name': 'Primary Information',
            'slug': 'basic',
        },
    }),
    ('general', {
        'name': 'General Information',
        'form': ProfileGeneralForm,
        'relevant_warning': False,
        'primary_fields_required': True,
        'group': {
            'name': 'Primary Information',
            'slug': 'general',
        },
    }),
    ('curriculum-vitae', {
        'name': 'Curriculum Vitae',
        'formset_model': CurriculumVitae,
        'formset_form': CurriculumVitaeForm,
        'type': 'Primary Information',
        'primary_fields_required': True,
        'group': {
            'name': 'Primary Information',
            'slug': 'curriculum-vitae',
        },
    }),
    ('documents', {
        'name': 'Documents',
        'formset_model': Document,
        'type': 'Primary Information',
        'group': {
            'name': 'Primary Information',
            'slug': 'documents',
        },
        'message': (
            'Please upload all relevant documents such as references, qualifications and '
            'certification.'
        )
    }),
    ('previous-work', {
        'name': 'Previous Work',
        'formset_model': PreviousWork,
        'formset_form': PreviousWorkForm,
        'primary_fields_required': True,
        'relevant_warning': False,
        'group': {
            'name': 'Primary Information',
            'slug': 'previous-work',
        },
        'readonly_fields': ['rank', 'company', 'date_from', 'date_to']
    }),
    ('photograph', {
        'name': 'Photograph',
        'form': ProfilePhotoForm,
        'primary_fields_required': True,
        'group': {
            'name': 'Primary Information',
            'slug': 'photograph',
        },
    }),
    ('languages', {
        'name': 'Languages',
        'formset_model': LanguageProficiency,
        'formset_form': LanguageProficiencyForm,
        'relevant_warning': True,
        'group': {
            'name': 'Secondary Information',
            'slug': 'languages',
        },
    }),
    ('travel', {
        'name': 'Travel Documents',
        'form': ProfileTravelForm,
        'relevant_warning': True,
        'group': {
            'name': 'Secondary Information',
            'slug': 'travel',
        }
    }),
    ('partner-and-references', {
        'name': 'Partner\'s Details',
        'form': ProfilePartnerReferencesForm,
        'relevant_warning': True,
        'group': {
            'name': 'Secondary Information',
            'slug': 'partner-and-references',
        }
    }),
    ('medical', {
        'name': 'Seafarer\'s Medical',
        'form': ProfileMedicalForm,
        'relevant_warning': True,
        'group': {
            'name': 'Secondary Information',
            'slug': 'medical',
        }
    }),
    ('additonal-certification', {
        'name': 'Education & Certification',
        'formset_model': OtherCertification,
        'formset_form': OtherCertificationForm,
        'group': {
            'name': 'Certificates and Education',
            'slug': 'additonal-certification',
        },
        'message': (
            'Please complete this section by adding any relevant Educational Qualifications you '
            'may hold. If we do not have your qualification, please do not hesitate to contact us.'
        ),
        'readonly_fields': ['certificate', 'issue_date', 'expiry_date']
    }),
    ('marine-certification', {
        'name': 'Marine Certification',
        'formset_model': MarineCertification,
        'formset_form': MarineCertificationForm,
        'marine_warning': True,
        'group': {
            'name': 'Certificates and Education',
            'slug': 'marine-certification',
        },
        'readonly_fields': ['certificate', 'issue_date', 'expiry_date']
    }),
    ('certificate-competency', {
        'name': 'Certificate of Competency',
        'formset_model': CompetencyCertificate,
        'formset_form': CompetencyCertificationForm,
        'relevant_warning': False,
        'marine_warning': True,
        'group': {
            'name': 'Certificates and Education',
            'slug': 'certificate-competency',
        },
        'readonly_fields': ['certificate', 'issuing_authority', 'expiry_date']
    }),
    ('declaration', {
        'name': 'Declaration',
        'form': ProfileDeclarationForm,
        'group': {
            'name': 'Declaration',
            'slug': 'declaration',
        },
    }),
    ('recruiter', {
        'admin': True,
        'name': 'Recruiter Admin',
        'form': ProfileRecruiterAdminForm,
    }),
])


def profile_edit(
    request, section, user, template, readonly=False, recruiter=False, extra_context=None
):

    # Do copy of oringal EDIT_FORMS as we don't want to change structure of EDIT_FORMS
    # remove profile from EDIT_FORMS as no need for user.
    COPY_EDIT_FORMS = copy.deepcopy(EDIT_FORMS)

    if not recruiter and 'profile' in COPY_EDIT_FORMS:
        del COPY_EDIT_FORMS['profile']
        del COPY_EDIT_FORMS['recruiter']

    try:
        form_section = COPY_EDIT_FORMS[section]
    except KeyError:
        raise Http404

    # Help the section numbering
    edit_forms_keys = COPY_EDIT_FORMS.keys()
    form_number = edit_forms_keys.index(section) + 1

    form_class = form_section.get('form', None)
    formset_model = form_section.get('formset_model', None)
    formset_form = form_section.get('formset_form', None)
    form = formset = None

    # User editing, or another user?
    selfedit = request.user == user

    # Don't allow certain pages to be self edited
    if not recruiter and form_section.get('admin', False):
        raise Http404

    if form_class:
        form = form_class(request.POST or None, request.FILES or None, instance=user)

        if form.is_valid():
            if not user.profile_started:
                user.profile_started = True
                user.save()
                NewCandidate.objects.create(user=user)

            if selfedit and form.changed_data:
                change_message = 'Changed %s.' % (
                    get_text_list([x.replace('_', ' ') for x in form.changed_data], 'and'),)
                TimelineLogEntry.objects.create(
                    user=request.user, message_type=TimelineLogEntry.PROFILE_UPDATE,
                    message=change_message)

            form.save()

            if not recruiter:
                user.updated = timezone.now()
                user.save()

            messages.success(request, 'Profile updated.')

            if not recruiter:
                return HttpResponseRedirect(reverse('profiles:profile', kwargs={
                    'section': section,
                }))
            else:
                return HttpResponseRedirect(reverse('recruiter:profile-edit-readonly', kwargs={
                    'pk': user.pk,
                    'section': section,
                }))

    if formset_model is not None:

        formset_class_kwargs = {}

        # Custom form
        if formset_form is not None:
            formset_class_kwargs['form'] = formset_form

        extra = 0
        if readonly:
            formset_class = inlineformset_factory(
                get_user_model(), formset_model, extra=extra, **formset_class_kwargs
            )
        else:
            if user.curriculumvitae_set.count() == 0:
                extra = 1

            formset_class = inlineformset_factory(
                get_user_model(), formset_model, extra=extra, **formset_class_kwargs
            )
        if request.POST:
            formset = formset_class(
                request.POST or None, request.FILES or None, instance=user
            )
            if formset.is_valid():
                formset.save()

                if not user.profile_started:
                    user.profile_started = True
                    user.save(update_fields=['profile_started'])
                    NewCandidate.objects.create(user=user)

                if not recruiter:
                    user.updated = timezone.now()
                    user.save(update_fields=['updated'])

                messages.success(request, 'Profile updated.')

                if recruiter:
                    return HttpResponseRedirect(reverse('recruiter:profile-edit-readonly', kwargs={
                        'pk': user.pk,
                        'section': section,
                    }))
                else:
                    return HttpResponseRedirect(reverse('profiles:profile', kwargs={
                        'section': section,
                    }))
        else:
            formset = formset_class(instance=user)

    status_form = ProfileStatusForm(instance=request.user)

    if readonly:
        if hasattr(formset, 'forms'):
            for formset_form in formset.forms:
                if 'id' in formset_form.fields:
                    del formset_form.fields['id']
                if 'user' in formset_form.fields:
                    del formset_form.fields['user']
                if 'DELETE' in formset_form.fields:
                    del formset_form.fields['DELETE']

    context = {
        'active_section': section,
        'form': form,
        'form_number': form_number,
        'form_section': form_section,
        'formset': formset,
        'marine_warning': form_section.get('marine_warning', False),
        'profile': user,
        'profile_detail': form_section.get('profile_detail', False),
        'profile_forms': COPY_EDIT_FORMS,
        'readonly': readonly,
        'recruiter': recruiter,
        'relevant_warning': form_section.get('relevant_warning', False),
        'primary_fields_required': form_section.get('primary_fields_required', False),
        'section': section,
        'selfedit': selfedit,
        'status_form': status_form,
    }
    if extra_context:
        context.update(extra_context)

    return TemplateResponse(request, template, context)


def unique_upload_path(instance, filename):
    """ Unique upload path for files."""
    now = timezone.now()
    current_site = Site.objects.get_current()
    hour_minute_second = now.strftime('%H_%M_%S')

    return u'uploads/{}/{}/{}/{}/{}/{}/{}/{}'.format(
        instance._meta.app_label,
        instance._meta.module_name,
        current_site.domain,
        now.strftime('%Y'),
        now.strftime('%m'),
        now.strftime('%d'),
        hour_minute_second,
        filename,
    )

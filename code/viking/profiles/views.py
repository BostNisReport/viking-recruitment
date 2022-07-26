# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator, InvalidPage
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import TimelineLogEntry, Message, StatusUpdate
from .forms import MessageForm, ProfileStatusForm
from .utils import profile_edit


@login_required
def dashboard(request):
    message = Message(user=request.user)
    message_form = MessageForm(instance=message)
    status_form = ProfileStatusForm(instance=request.user)

    if request.GET.get('action') == 'message':
        message_form = MessageForm(request.POST or None, instance=message)

        if message_form.is_valid():
            message_form.save()
            messages.success(request, 'Message added to your timeline.')
            return HttpResponseRedirect(reverse('profiles:dashboard'))

    elif request.GET.get('action') == 'status':
        status_form = ProfileStatusForm(request.POST or None, instance=request.user)
        previous_status = request.user.status

        if status_form.is_valid():
            status_form.save()

            if request.user.status != previous_status:
                StatusUpdate.objects.create(user=request.user, status=status_form.cleaned_data['status'])

            return HttpResponseRedirect(reverse('profiles:dashboard'))

    log_entries = TimelineLogEntry.objects.filter(user=request.user, message_type__lte=100)
    paginator = Paginator(log_entries, 10)

    try:
        page_obj = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404

    return TemplateResponse(request, 'profiles/dashboard.html', {
        'message_form': message_form,
        'status_form': status_form,
        'page_obj': page_obj,
        'paginator': paginator,
    })


@login_required
def user_profile_edit_home(request):
    return user_profile_edit(request, 'basic')


@login_required
def user_profile_home(request):
    """ This extra view for just readonly. """
    return user_profile_edit(request, section='basic', readonly=True)


@login_required
def user_profile(request, section):
    """ This extra view for just readonly. """
    return user_profile_edit(request, section=section, readonly=True)


@login_required
def user_profile_edit(request, section, readonly=False):
    return profile_edit(
        request=request,
        section=section,
        user=request.user,
        template='profiles/profile_edit.html',
        readonly=readonly,
    )

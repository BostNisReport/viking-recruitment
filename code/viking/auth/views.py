# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic import CreateView, TemplateView

from viking.profiles.models import PreviousWork

from .emails import send_activation_email, send_welcome_email
from .forms import get_registration_form
from .models import BannedIP


@login_required
def profile_redirect(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('admin:index'))
    elif request.user.has_perm('jobs.recruiter_staff'):
        return HttpResponseRedirect(reverse('recruiter:dashboard'))
    else:
        return HttpResponseRedirect(reverse('profiles:dashboard'))


class BannedView(TemplateView):
    template_name = 'registration/banned.html'


class UserRegistrationFormView(CreateView):
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('registration_complete')

    def get_form_class(self):
        return get_registration_form(self.request)

    def form_valid(self, form):
        redirect = super(UserRegistrationFormView, self).form_valid(form)
        latest_position = self.request.POST['latest_position']
        PreviousWork.objects.create(
            user=self.object,
            company=latest_position
        )
        send_activation_email(self.request, self.object)
        return redirect


class RegistrationCompleteView(TemplateView):
    template_name = 'registration/registration_complete.html'


def activate(request, pk, activation_key):
    UserModel = get_user_model()

    # Check for permanent bans
    try:
        BannedIP.objects.get(ip_address=request.META['REMOTE_ADDR'])
        return HttpResponseRedirect(reverse('registration_banned'))
    except BannedIP.DoesNotExist:
        pass

    try:
        user = get_user_model().objects.get(pk=pk)

        # Activate the account if the key matches
        if user.activation_key and user.activation_key == activation_key:
            user.is_active = True
            user.activation_key = ''
            user.save()
            send_welcome_email(request, user)
            return HttpResponseRedirect(reverse('registration_activate_complete'))
    except UserModel.DoesNotExist:
        pass

    return TemplateResponse(request, 'registration/activate_failed.html')


class ActivateCompleteView(TemplateView):
    template_name = 'registration/activate_complete.html'

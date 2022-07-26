from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
import datetime
from dateutil.relativedelta import relativedelta


def form_to_dict(form):
    form_dict = {}

    # Common prefix for form
    if form.prefix:
        field_prefix = '%s-' % (form.prefix,)
    else:
        field_prefix = ''

    for i in form:
        field_name = '%s%s' % (field_prefix, i.name)
        form_dict[field_name] = i.value()

    return form_dict


def search_dict_list(search_qs_dict):
    search_qs = []

    for k, v in search_qs_dict.iteritems():
        if isinstance(v, list):
            for i in v:
                search_qs.append((k, i.encode('utf-8')))
        elif isinstance(v, bool):
            if v:
                v = 'on'
            else:
                v = ''
            search_qs.append((k, v))
        elif v is None:
            pass
        else:
            search_qs.append((k, v.encode('utf-8')))

    return search_qs


def age_to_date(value):
    return datetime.date.today() - relativedelta(years=value)


def email_user_message(user, message, request=None, job=None):
    if request is not None:
        protocol = 'https' if request.is_secure() else 'http'
    else:
        protocol = 'http'

    email_subject = 'New message from Viking Recruitment'
    email_body = render_to_string('recruiter/email_message.txt', {
        'protocol': protocol,
        'site': Site.objects.get_current(),
        'message': message,
    })
    email_html = render_to_string('recruiter/email_message.html', {
        'protocol': protocol,
        'site': Site.objects.get_current(),
        'message': message,
        'job': job,
    })

    email = EmailMultiAlternatives(email_subject, email_body, to=[user.email])
    email.attach_alternative(email_html, 'text/html')
    email.send()

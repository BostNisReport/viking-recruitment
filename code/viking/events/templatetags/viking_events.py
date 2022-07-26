from django import template
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from blanc_basic_events.events.models import Event
from blanc_basic_events.events.utils import sorted_event_list

register = template.Library()


@register.assignment_tag
def get_upcoming_viking_events(limit=None):
    start_date = timezone.now()
    end_date = start_date + relativedelta(years=+2)
    return sorted_event_list(start_date=start_date, end_date=end_date, queryset=Event.objects.exclude(category__slug='come-and-see-us'), limit=limit)


@register.assignment_tag
def get_upcoming_viking_come_and_see_events(limit=None):
    start_date = timezone.now()
    end_date = start_date + relativedelta(years=+2)
    return sorted_event_list(start_date=start_date, end_date=end_date, queryset=Event.objects.filter(category__slug='come-and-see-us'), limit=limit)

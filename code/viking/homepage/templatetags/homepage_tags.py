from django import template
from viking.homepage.models import Banner

register = template.Library()


@register.assignment_tag
def get_homepage_banners():
    return Banner.objects.filter(published=True)

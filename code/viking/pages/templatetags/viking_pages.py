from django import template
from django.core.urlresolvers import reverse
from viking.pages.models import FooterImage, HeaderLink, FooterLink, MenuItem

register = template.Library()


@register.assignment_tag
def get_footer_images(count=None):
    images = FooterImage.objects.all()

    if count is not None:
        images = images[:count]

    return images


@register.assignment_tag
def get_header_links():
    return HeaderLink.objects.all()


@register.assignment_tag
def get_footer_links():
    return FooterLink.objects.all()


@register.assignment_tag
def get_root_menuitems():
    return MenuItem.objects.root_nodes()


@register.assignment_tag
def get_page_ancestor_ids(current_page=None, current_url=None):
    menu_item = None

    try:
        if current_url:
            menu_item = MenuItem.objects.get(url=reverse(current_url))
        elif current_page:
            menu_item = MenuItem.objects.get(url=current_page.url)
    except MenuItem.DoesNotExist:
        pass

    if menu_item:
        return menu_item.get_ancestors(include_self=True).values_list('id', flat=True)
    else:
        return []

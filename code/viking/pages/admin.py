from adminsortable.admin import SortableAdmin
from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import FooterImage, FooterLink, HeaderLink, LargeBanner, MenuItem, SmallBanner


@admin.register(FooterImage)
class FooterImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'position')
    list_editable = ('position',)


@admin.register(LargeBanner, SmallBanner)
class BannerAdmin(admin.ModelAdmin):
    search_fields = ('title',)


@admin.register(FooterLink, HeaderLink)
class LinkAdmin(SortableAdmin):
    pass


@admin.register(MenuItem)
class MenuItemAdmin(DjangoMpttAdmin):
    pass

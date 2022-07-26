# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Language, AdvertReference, Country, NationalityGroup


class LanguageAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class AdvertReferenceAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'published')
    list_editable = ('published',)
    list_filter = ('published',)


admin.site.register(Language, LanguageAdmin)
admin.site.register(AdvertReference, AdvertReferenceAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'iso_3166_1_a2', 'iso_3166_1_a3', 'iso_3166_1_numeric', 'display_order',
    )

    search_fields = ('name', 'iso_3166_1_a2', 'iso_3166_1_a3', 'iso_3166_1_numeric',)

    fieldsets = (
        (
            'Details', {
                'fields': (
                    'name', 'iso_3166_1_a2', 'iso_3166_1_a3', 'iso_3166_1_numeric',
                    'display_order',
                )
            }
        ),
    )
admin.site.register(Country, CountryAdmin)


class NationalityGroupAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)
    filter_horizontal = ('countries',)

    fieldsets = (
        (
            'Details', {
                'fields': (
                    'name', 'countries',
                )
            }
        ),
        (
            'Meta data', {
                'classes': ('collapse',),
                'fields': ('id',)
            }
        ),
    )
    readonly_fields = ('id',)
admin.site.register(NationalityGroup, NationalityGroupAdmin)

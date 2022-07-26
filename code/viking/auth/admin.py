# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import VikingUser, BannedIP
from .csvexport import CSVExportMixin
from forms import VikingUserChangeForm, UserCreationForm
from viking.profiles.models import LanguageProficiency


class LanguageProficiencyInline(admin.TabularInline):
    model = LanguageProficiency
    extra = 0


class GroupListFilter(admin.SimpleListFilter):
    title = 'Group'
    parameter_name = 'group'

    def lookups(self, request, model_admin):
        return Group.objects.values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(groups__id=self.value())


class VikingUserAdmin(CSVExportMixin, UserAdmin):
    fieldsets = (
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Password', {
            'fields': ('password',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': (
                'last_login', 'date_joined', 'prompt_email_sent', 'prompt_email_sent_date',
            )
        }),
    )
    add_fieldsets = (
        ('Personal details', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Password', {
            'classes': ('wide',),
            'fields': ('password1', 'password2')
        }),
    )
    form = VikingUserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', GroupListFilter)
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('-id',)
    date_hierarchy = 'date_joined'
    inlines = [LanguageProficiencyInline]
    csvexport_fields = (
        'id', 'title', 'first_name', 'last_name', 'email', 'nationality', 'send_email',
        'date_joined'
    )
    readonly_fields = (
        'prompt_email_sent', 'prompt_email_sent_date', 'date_joined', 'updated'
    )

    def get_export_queryset(self, request):
        return VikingUser.objects.only(*self.csvexport_fields).filter(profile_started=True)


class BannedIPAdmin(admin.ModelAdmin):
    search_fields = ('ip_address',)
    list_display = ('ip_address', 'added')
    list_filter = ('added',)
    date_hierarchy = 'added'


admin.site.register(VikingUser, VikingUserAdmin)
admin.site.register(BannedIP, BannedIPAdmin)

from django.contrib import admin
from blanc_pages import block_admin
from models import *


class GroupAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    prepopulated_fields = {
        'slug': ('title',)
    }


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'group', 'company_title', 'company_subtitle', 'image'),
        }),
        ('Profile', {
            'fields': ('visible_profile', 'content', 'phone_number', 'office'),
        }),
        ('Advanced options', {
            'fields': ('slug', 'position', 'published'),
        }),
    )
    search_fields = ('name',)
    list_filter = ('group',)
    list_display = ('name', 'group', 'position')
    list_editable = ('position',)
    prepopulated_fields = {
        'slug': ('name',)
    }


class ContactProfileInline(block_admin.StackedInline):
    model = ContactProfile
    extra = 1


class ContactBlockAdmin(block_admin.BlockModelAdmin):
    inlines = [ContactProfileInline]


admin.site.register(Group, GroupAdmin)
admin.site.register(Profile, ProfileAdmin)
block_admin.site.register(ContactBlock, ContactBlockAdmin)
block_admin.site.register_block(ContactBlock, 'Viking Recruitment')

from django.contrib import admin
from models import *


class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'position', 'published')
    list_editable = ('position', 'published')
    list_filter = ('published',)


admin.site.register(Banner, BannerAdmin)

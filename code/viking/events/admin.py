from django.contrib import admin
from blanc_basic_events.events.models import Event
from blanc_basic_events.events.admin import EventAdmin
from models import *
from blanc_pages import block_admin


class VikingEventAdmin(EventAdmin):
    inlines = ()


admin.site.unregister(Event)
admin.site.register(Event, VikingEventAdmin)

block_admin.site.register(LatestEventsBlock)
block_admin.site.register_block(LatestEventsBlock, 'Viking Recruitment')

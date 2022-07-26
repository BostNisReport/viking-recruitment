from django.db import models
from blanc_pages.blocks import BaseBlock


class LatestEventsBlock(BaseBlock):
    number_of_events = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'latest events'

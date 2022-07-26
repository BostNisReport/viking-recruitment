from django.db import models
from blanc_pages.blocks import BaseBlock


class LatestNewsPostsBlock(BaseBlock):
    number_of_posts = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'latest news posts'

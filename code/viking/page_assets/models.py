from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from blanc_pages.blocks import BaseBlock


@python_2_unicode_compatible
class SmallBannerBlock(BaseBlock):
    banner = models.ForeignKey('viking_pages.SmallBanner', null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'banner - small'

    def __str__(self):
        return '%s' % (self.banner or 'Small Banner',)


@python_2_unicode_compatible
class LargeBannerBlock(BaseBlock):
    banner = models.ForeignKey('viking_pages.LargeBanner', null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'banner - large'

    def __str__(self):
        return '%s' % (self.banner or 'Large Banner',)


class RelatedLinkListBlock(BaseBlock):
    class Meta:
        verbose_name = 'related links'


@python_2_unicode_compatible
class RelatedLink(models.Model):
    related_link_list = models.ForeignKey(RelatedLinkListBlock)
    title = models.CharField(max_length=100)
    url = models.URLField('URL')
    position = models.PositiveSmallIntegerField(default=1, db_index=True)

    class Meta:
        ordering = ('position',)

    def __str__(self):
        return self.title


class LatestTweetsBlock(BaseBlock):
    class Meta:
        verbose_name = 'latest tweets'

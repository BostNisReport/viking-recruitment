from __future__ import unicode_literals

from adminsortable.models import Sortable
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from mptt.models import MPTTModel, TreeForeignKey


@python_2_unicode_compatible
class FooterImage(models.Model):
    COLOUR_CHOICES = (
        ('', 'White'),
        ('lightblue', 'Light Blue'),
        ('gold', 'Gold'),
        ('darkblue', 'Dark Blue'),
    )

    title = models.CharField(max_length=100, db_index=True)
    image = models.ImageField(
        upload_to='pages/footerimage', height_field='image_height', width_field='image_width')
    image_height = models.PositiveIntegerField(editable=False)
    image_width = models.PositiveIntegerField(editable=False)
    link = models.URLField()
    header_colour = models.CharField(max_length=10, choices=COLOUR_CHOICES, blank=True)
    subhead_colour = models.CharField(max_length=10, choices=COLOUR_CHOICES, blank=True)
    header = models.TextField()
    subhead_text = models.TextField()
    subheader = models.CharField(max_length=100)
    position = models.PositiveSmallIntegerField(default=1, db_index=True)

    class Meta:
        ordering = ('position',)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Banner(models.Model):
    COLOUR_CHOICES = (
        ('red', 'Red'),
        ('gold', 'Gold'),
        ('lightblue', 'Light Blue'),
        ('grey', 'Grey'),
        ('darkblue', 'Dark Blue'),
    )

    title = models.CharField(max_length=100, db_index=True)
    header_colour = models.CharField(max_length=10, choices=COLOUR_CHOICES)
    image = models.ImageField(
        upload_to='pages/banner', height_field='image_height', width_field='image_width')
    image_height = models.PositiveIntegerField(editable=False)
    image_width = models.PositiveIntegerField(editable=False)
    link = models.URLField()
    content = models.TextField()

    class Meta:
        abstract = True
        ordering = ('title',)

    def __str__(self):
        return self.title


class LargeBanner(Banner):
    pass


class SmallBanner(Banner):
    pass


@python_2_unicode_compatible
class Link(Sortable):
    title = models.CharField(max_length=100, db_index=True)
    link = models.URLField()

    class Meta(Sortable.Meta):
        abstract = True

    def __str__(self):
        return self.title


class HeaderLink(Link):
    pass


class FooterLink(Link):
    pass


@python_2_unicode_compatible
class MenuItem(MPTTModel):
    title = models.CharField(max_length=100)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    url = models.CharField('URL', max_length=100, blank=True, db_index=True)

    def __str__(self):
        return '%s -- %s' % (self.title, self.url)

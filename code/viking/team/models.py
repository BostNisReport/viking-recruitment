from __future__ import unicode_literals

from django.db import models
from blanc_pages.blocks import BaseBlock


class Group(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('team:group-detail', (), {
            'slug': self.slug,
        })


class ProfileManager(models.Manager):
    def published(self):
        return self.get_query_set().filter(published=True)


class Profile(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    email = models.EmailField()
    group = models.ForeignKey(Group)
    company_title = models.CharField(max_length=100)
    company_subtitle = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='team/profile', height_field='image_height', width_field='image_width', blank=True)
    image_height = models.PositiveIntegerField(null=True, editable=False)
    image_width = models.PositiveIntegerField(null=True, editable=False)
    visible_profile = models.BooleanField(default=False)
    content = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    office = models.CharField(max_length=50, blank=True)
    position = models.PositiveSmallIntegerField(default=1, db_index=True)
    published = models.BooleanField(default=True, db_index=True)

    objects = ProfileManager()

    class Meta:
        ordering = ('position', 'name')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('team:profile-detail', (), {
            'slug': self.slug,
        })


class ContactBlock(BaseBlock):
    class Meta:
        verbose_name = 'contact'


class ContactProfile(models.Model):
    contact_list = models.ForeignKey(ContactBlock)
    profile = models.ForeignKey(Profile)
    position = models.PositiveSmallIntegerField(default=1, db_index=True)

    class Meta:
        ordering = ('position',)

    def __unicode__(self):
        if self.profile:
            return unicode(self.profile)
        else:
            return u''

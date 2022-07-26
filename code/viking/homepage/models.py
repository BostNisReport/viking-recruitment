from __future__ import unicode_literals

from django.db import models


class Banner(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='homepage/banner', height_field='image_height', width_field='image_width')
    image_height = models.PositiveIntegerField(editable=False, null=True)
    image_width = models.PositiveIntegerField(editable=False, null=True)
    link = models.URLField()
    coloured_link_text = models.CharField(max_length=100)
    link_text = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    position = models.PositiveIntegerField(default=1, db_index=True)
    published = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ('position',)

    def __unicode__(self):
        return self.title

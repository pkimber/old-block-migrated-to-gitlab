# -*- encoding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import models

import reversion

from block.models import (
    BlockModel,
    ContentModel,
    Image,
    Link,
    Wizard,
)


class TitleBlock(BlockModel):
    pass

reversion.register(TitleBlock)


class Title(ContentModel):

    block = models.ForeignKey(TitleBlock, related_name='content')
    order = models.IntegerField()
    title = models.TextField()
    picture = models.ForeignKey(
        Image,
        related_name='title_picture',
        blank=True, null=True
    )
    link = models.ForeignKey(
        Link,
        related_name='title_link',
        blank=True, null=True
    )
    slideshow = models.ManyToManyField(
        Image,
        related_name='slideshow',
        through='TitleImage'
    )

    class Meta:
        # cannot put 'unique_together' on abstract base class
        # https://code.djangoproject.com/ticket/16732
        unique_together = ('block', 'moderate_state')
        verbose_name = 'Test content'
        verbose_name_plural = 'Test contents'

    def __str__(self):
        return '{} ({}, {})'.format(
            self.title, self.order, self.moderate_state.name
        )

    def copy_related_data(self, published_instance):
        """Copy slideshow images."""
        for image in self.slideshow.all():
            published_instance.slideshow.add(image)

    def url_publish(self):
        return reverse('example.title.publish', kwargs={'pk': self.pk})

    def url_remove(self):
        return reverse('example.title.remove', kwargs={'pk': self.pk})

    def url_update(self):
        return reverse('example.title.update', kwargs={'pk': self.pk})

    @property
    def wizard_fields(self):
        return [
            Wizard('picture', Wizard.IMAGE, Wizard.SINGLE),
            Wizard('link', Wizard.LINK, Wizard.SINGLE),
            Wizard('slideshow', Wizard.IMAGE, Wizard.MULTI),
        ]

reversion.register(Title)


class TitleImage(models.Model):
    """Slideshow images for the title.

    This is the model that is used to govern the many-to-many relationship
    between ``Title`` and ``Image``.

    https://docs.djangoproject.com/en/1.8/topics/db/models/#extra-fields-on-many-to-many-relationships

    """
    content_obj = models.ForeignKey(Title)
    image = models.ForeignKey(Image)
    order = models.IntegerField()

    class Meta:
        verbose_name = 'Title Image'
        verbose_name_plural = 'Title Images'

reversion.register(TitleImage)

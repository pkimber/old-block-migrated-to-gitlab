# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models

import reversion

from block.models import (
    BlockModel,
    ContentModel,
)


class TitleBlock(BlockModel):
    pass

reversion.register(TitleBlock)


class Title(ContentModel):

    block = models.ForeignKey(TitleBlock, related_name='content')
    order = models.IntegerField()
    title = models.TextField()

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

    def url_publish(self):
        return reverse('example.title.publish', kwargs={'pk': self.pk})

    def url_remove(self):
        return reverse('example.title.remove', kwargs={'pk': self.pk})

    def url_update(self):
        return reverse('example.title.update', kwargs={'pk': self.pk})

reversion.register(Title)

# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import collections

from datetime import datetime

from django.conf import settings
from django.db import models

import reversion

from base.model_utils import TimeStampedModel


def default_moderate_state():
    return ModerateState.pending()


class BlockError(Exception):

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr('%s, %s' % (self.__class__.__name__, self.value))


class ModerateState(models.Model):
    """Accept, remove or pending."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = 'Moderate'
        verbose_name_plural = 'Moderated'

    def __str__(self):
        return '{}'.format(self.name)

    @staticmethod
    def pending():
        return ModerateState.objects.get(slug='pending')

    @staticmethod
    def published():
        return ModerateState.objects.get(slug='published')

    @staticmethod
    def removed():
        return ModerateState.objects.get(slug='removed')

reversion.register(ModerateState)


class PageManager(models.Manager):

    def menu(self):
        """Return page objects for a menu."""
        return self.model.objects.all().order_by('order')


class Page(TimeStampedModel):
    """Which page on the web site.

    An order of zero (0) indicates that the page should be excluded from a
    menu.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    order = models.IntegerField(default=0)
    is_home = models.BooleanField(default=False)
    objects = PageManager()

    class Meta:
        ordering = ['name']
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __str__(self):
        return '{}'.format(self.name)

reversion.register(Page)


class Section(TimeStampedModel):
    """Section of the page e.g. content, header, footer."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

    def __str__(self):
        return '{}'.format(self.name)

reversion.register(Section)


class ContentManager(models.Manager):

    def pending(self, page, section, kwargs=None):
        """Return a list of pending content for a section.

        Note: we return a list of content instances not a queryset.

        """
        pending = ModerateState.pending()
        published = ModerateState.published()
        qs = self.model.objects.filter(
            block__page=page,
            block__section=section,
            moderate_state__in=[published, pending],
        )
        order_by = None
        if kwargs:
            order_by = kwargs.pop('order_by', None)
            qs = qs.filter(**kwargs)
        if order_by:
            qs = qs.order_by(order_by)
        else:
            qs = qs.order_by('order')
        result = collections.OrderedDict()
        for c in qs:
            if c.block.pk in result:
                if c.moderate_state == pending:
                    result[c.block.pk] = c
            else:
                result[c.block.pk] = c
        return list(result.values())

    def published(self, page, section):
        """Return a published content for a page."""
        published = ModerateState.published()
        return self.model.objects.filter(
            block__page=page,
            block__section=section,
            moderate_state=published,
        ).order_by(
            'order',
        )


class BlockModel(TimeStampedModel):
    """Abstract base class for blocks of one type."""

    page = models.ForeignKey(Page)
    section = models.ForeignKey(Section)

    class Meta:
        abstract = True
        verbose_name = 'Block'
        verbose_name_plural = 'Blocks'

    def __str__(self):
        return '{}: page {}, section {}'.format(
            self.pk, self.page.name, self.section.name
        )


class ContentModel(TimeStampedModel):
    """Abstract base class for the content within blocks.

    TODO rename to 'ContentModel'?
    """
    moderate_state = models.ForeignKey(
        ModerateState,
        default=default_moderate_state
    )
    date_moderated = models.DateTimeField(blank=True, null=True)
    user_moderated = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='+'
    )
    objects = ContentManager()

    class Meta:
        abstract = True
        verbose_name = 'Block content'
        verbose_name_plural = 'Block contents'

    def __str__(self):
        return '{}'.format(self.pk)

    def _delete_removed_content(self):
        """delete content which was previously removed."""
        try:
            c = self.block.content.get(
                moderate_state=ModerateState.removed()
            )
            c.delete()
        except self.DoesNotExist:
            pass

    def _is_pending(self):
        return self.moderate_state == ModerateState.pending()
    is_pending = property(_is_pending)

    def _is_published(self):
        return self.moderate_state == ModerateState.published()
    is_published = property(_is_published)

    def _is_removed(self):
        return self.moderate_state == ModerateState.removed()
    is_removed = property(_is_removed)

    def _set_moderated(self, user, moderate_state):
        self.date_moderated = datetime.now()
        self.user_moderated = user
        self.moderate_state = moderate_state

    def _set_published_to_remove(self, user):
        """publishing new content, so remove currently published content."""
        try:
            c = self.block.content.get(
                moderate_state=ModerateState.published()
            )
            c.set_removed(user)
            c.save()
        except self.DoesNotExist:
            pass

    def set_pending(self, user):
        if self.moderate_state == ModerateState.published():
            try:
                self.block.content.get(
                    moderate_state=ModerateState.pending()
                )
                raise BlockError(
                    "Section already has pending content so "
                    "published content should not be edited."
                )
            except self.DoesNotExist:
                self._set_moderated(user, ModerateState.pending())
                self.pk = None
        elif self.moderate_state == ModerateState.pending():
            return
        else:
            raise BlockError(
                "Cannot edit content which has been removed"
            )

    def set_published(self, user):
        """Publish content."""
        if not self.moderate_state == ModerateState.pending():
            raise BlockError(
                "Cannot publish content unless it is 'pending'"
            )
        self._delete_removed_content()
        self._set_published_to_remove(user)
        self._set_moderated(user, ModerateState.published())

    def set_removed(self, user):
        """Remove content."""
        if self.moderate_state == ModerateState.removed():
            raise BlockError(
                "Cannot remove content which has already been removed"
            )
        self._delete_removed_content()
        self._set_moderated(user, ModerateState.removed())

# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import collections

from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models import Max

import reversion

from base.model_utils import (
    copy_model_instance,
    TimeStampedModel,
)


PENDING = 'pending'
PUBLISHED = 'published'
REMOVED = 'removed'


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
    def _get_published():
        """Internal use only."""
        return ModerateState.objects.get(slug='published')

    @staticmethod
    def pending():
        return ModerateState.objects.get(slug=PENDING)

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

    def next_order(self):
        result = self.model.objects.aggregate(max_order=Max('order'))
        max_order = result.get('max_order', 0)
        if max_order == 0:
            raise BlockError(
                "Cannot get the maximum value of the 'order' field "
                "in the '{}' class.".format(self.model.__name__)
            )
        elif max_order:
            return max_order + 1
        else:
            return 1

    def pending(self, page, section, kwargs=None):
        """Return a list of pending content for a section.

        Note: we return a list of content instances not a queryset.

        """
        pending = ModerateState.pending()
        published = ModerateState._get_published()
        qs = self.model.objects.filter(
            block__page=page,
            block__section=section,
            moderate_state=pending,
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
        published = ModerateState._get_published()
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
    """Abstract base class for the content within blocks."""

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

    def _copy_pending_to_published(self, pending, user):
        """Copy the pending record to a new published record."""
        c = copy_model_instance(pending)
        c._set_moderated(user, ModerateState._get_published())
        c.save()
        return c

    #def _delete_pending_content(self):
    #    """delete pending content."""
    #    try:
    #        c = self._get_pending()
    #        c.delete()
    #    except self.DoesNotExist:
    #        pass

    def _delete_published_content(self):
        """delete published content."""
        try:
            c = self._get_published()
            c.delete()
        except self.DoesNotExist:
            pass

    def _delete_removed_content(self):
        """delete content which was previously removed."""
        try:
            c = self._get_removed()
            c.delete()
        except self.DoesNotExist:
            pass

    def _get_pending(self):
        return self.block.content.get(
            moderate_state=ModerateState.pending()
        )

    def _get_published(self):
        return self.block.content.get(
            moderate_state=ModerateState._get_published()
        )

    def _get_removed(self):
        return self.block.content.get(
            moderate_state=ModerateState.removed()
        )

    def _is_pending(self):
        return self.moderate_state == ModerateState.pending()
    is_pending = property(_is_pending)

    def _is_published(self):
        return self.moderate_state == ModerateState._get_published()
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
            c = self._get_published()
            c._set_moderated(user, ModerateState.removed())
            c.save()
        except self.DoesNotExist:
            pass

    #def set_pending(self, user):
    #    if self.moderate_state == ModerateState._get_published():
    #        try:
    #            self.block.content.get(
    #                moderate_state=ModerateState.pending()
    #            )
    #            raise BlockError(
    #                "Section already has pending content so "
    #                "published content should not be edited."
    #            )
    #        except self.DoesNotExist:
    #            self._set_moderated(user, ModerateState.pending())
    #            self.pk = None
    #    elif self.moderate_state == ModerateState.pending():
    #        return
    #    else:
    #        raise BlockError(
    #            "Cannot edit content which has been removed"
    #        )

    def publish(self, user):
        """Publish content.

        Return the published content.

        """
        try:
            pending = self._get_pending()
        except self.DoesNotExist:
            raise BlockError(
                "Cannot publish content unless it is 'pending'"
            )
        self._delete_removed_content()
        self._set_published_to_remove(user)
        return self._copy_pending_to_published(pending, user)

    def remove(self, user):
        """Remove content."""
        pending = None
        published = None
        try:
            pending = self._get_pending()
        except self.DoesNotExist:
            pass
        try:
            published = self._get_published()
        except self.DoesNotExist:
            pass
        if not pending and not published:
            raise BlockError(
                "Cannot find pending or published content to remove."
            )
        self._delete_removed_content()
        if published:
            published._set_moderated(user, ModerateState.removed())
            published.save()
            if pending:
                pending.delete()
        else:
            pending._set_moderated(user, ModerateState.removed())
            pending.save()

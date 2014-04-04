# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import (
    models,
    transaction,
)
from django.db.models import Max

import reversion

from base.model_utils import (
    copy_model_instance,
    TimeStampedModel,
)

ADD = 'add'
EDIT = 'edit'
PUSH = 'push'

PENDING = 'pending'
PUBLISHED = 'published'
REMOVED = 'removed'


def _default_edit_state():
    return EditState._add()


def _default_moderate_state():
    return ModerateState._pending()


class BlockError(Exception):

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr('%s, %s' % (self.__class__.__name__, self.value))


class EditState(models.Model):
    """Add, pushed or editing."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = 'Edit state'
        verbose_name_plural = 'Edit state'

    def __str__(self):
        return '{}'.format(self.name)

    @staticmethod
    def _add():
        """Internal use only."""
        return EditState.objects.get(slug=ADD)

    @staticmethod
    def _edit():
        return EditState.objects.get(slug=EDIT)

    @staticmethod
    def _push():
        return EditState.objects.get(slug=PUSH)

reversion.register(EditState)


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
    def _published():
        """Internal use only."""
        return ModerateState.objects.get(slug=PUBLISHED)

    @staticmethod
    def _pending():
        return ModerateState.objects.get(slug=PENDING)

    @staticmethod
    def _removed():
        return ModerateState.objects.get(slug=REMOVED)

reversion.register(ModerateState)


class PageManager(models.Manager):

    def menu(self):
        """Return page objects for a menu."""
        return self.model.objects.all().order_by('order')


class Page(TimeStampedModel):
    """Which page on the web site.

    The 'slug_menu' is an optional field that can be used to add a page to a
    sub-menu e.g. 'training/faq'.  In this example, the 'slug_menu' would be
    set to 'faq'.

    An order of zero (0) indicates that the page should be excluded from a
    menu - see 'PageManager', 'menu' (although it doesn't look like it
    excludes items with an order of zero!).
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    slug_menu = models.SlugField(max_length=100, blank=True)
    order = models.IntegerField(default=0)
    is_home = models.BooleanField(default=False)
    template_name = models.CharField(max_length=150)
    objects = PageManager()

    class Meta:
        ordering = ['order', 'slug', 'slug_menu']
        unique_together = ('slug', 'slug_menu')
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return reverse('project.page.design', kwargs=self.get_url_kwargs())

    def get_url_kwargs(self):
        result = dict(page=self.slug,)
        if self.slug_menu:
            result.update(dict(menu=self.slug_menu,))
        return result


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

    def _delete_removed_content(self):
        """delete content which was previously removed."""
        try:
            c = self._get_removed()
            c.delete()
        except ObjectDoesNotExist:
            pass

    def _get_removed(self):
        return self.content.get(
            moderate_state=ModerateState._removed()
        )

    def _remove_published_content(self, user):
        """publishing new content, so remove currently published content."""
        try:
            c = self.get_published()
            c._set_moderated(user, ModerateState._removed())
            c.save()
        except ObjectDoesNotExist:
            pass

    def get_pending(self):
        """If the block has pending content, then get it."""
        return self.content.get(
            moderate_state=ModerateState._pending()
        )

    def get_published(self):
        """If the block has published content, then get it."""
        return self.content.get(
            moderate_state=ModerateState._published()
        )

    def publish(self, user):
        """Publish content."""
        try:
            pending = self.get_pending()
        except ObjectDoesNotExist:
            raise BlockError(
                "Cannot publish content unless it is 'pending'"
            )
        with transaction.atomic():
            self._delete_removed_content()
            self._remove_published_content(user)
            # copy the pending record to a new published record.
            published_instance = copy_model_instance(pending)
            published_instance._set_moderated(user, ModerateState._published())
            published_instance.save()
            # give pending class the opportunity to copy data
            pending.copy_related_data(published_instance)
            # mark the pending record as 'pushed' (published)
            pending.set_pending_pushed()
            pending.save()

    def remove(self, user):
        """Remove content.

        pending only - set pending to removed.
        published only - set published to removed.
        pending and published - delete pending, set published to removed.

        """
        pending = None
        published = None
        try:
            pending = self.get_pending()
        except ObjectDoesNotExist:
            pass
        try:
            published = self.get_published()
        except ObjectDoesNotExist:
            pass
        if not pending and not published:
            raise BlockError(
                "Cannot find pending or published content to remove."
            )
        with transaction.atomic():
            self._delete_removed_content()
            if published:
                published._set_moderated(user, ModerateState._removed())
                published.save()
                if pending:
                    pending.delete()
            else:
                pending._set_moderated(user, ModerateState._removed())
                pending.save()


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
        pending = ModerateState._pending()
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
        return qs

    def published(self, page, section):
        """Return a published content for a page."""
        published = ModerateState._published()
        return self.model.objects.filter(
            block__page=page,
            block__section=section,
            moderate_state=published,
        ).order_by(
            'order',
        )


class ContentModel(TimeStampedModel):
    """Abstract base class for the content within blocks.

    'pushed' is set to 'True' on a 'pending' model when it has just been
    'published'.  When the user edits the 'pending' record, the 'pushed'
    field is set to 'False'.

    """

    moderate_state = models.ForeignKey(
        ModerateState,
        default=_default_moderate_state
    )
    date_moderated = models.DateTimeField(blank=True, null=True)
    user_moderated = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='+'
    )
    edit_state = models.ForeignKey(
        EditState,
        default=_default_edit_state
    )
    objects = ContentManager()

    class Meta:
        abstract = True
        verbose_name = 'Block content'
        verbose_name_plural = 'Block contents'

    def __str__(self):
        return '{}'.format(self.pk)

    def _is_pending(self):
        return self.moderate_state == ModerateState._pending()
    is_pending = property(_is_pending)

    def _is_pending_added(self):
        return self.is_pending and self.edit_state == EditState._add()
    is_pending_added = property(_is_pending_added)

    def _is_pending_edited(self):
        return self.is_pending and self.edit_state == EditState._edit()
    is_pending_edited = property(_is_pending_edited)

    def _is_pending_pushed(self):
        return self.is_pending and self.edit_state == EditState._push()
    is_pending_pushed = property(_is_pending_pushed)

    def _is_published(self):
        return self.moderate_state == ModerateState._published()
    is_published = property(_is_published)

    def _is_removed(self):
        return self.moderate_state == ModerateState._removed()
    is_removed = property(_is_removed)

    def _set_moderated(self, user, moderate_state):
        self.date_moderated = datetime.now()
        self.user_moderated = user
        self.moderate_state = moderate_state

    def copy_related_data(self, published_instance):
        """Copy related data from this instance to the published instance.

        If the content type has many to many keys or elements
        e.g. accordion, then override this method to copy the data from
        'pending' to 'published'.

        """
        pass

    def has_elements(self):
        """If the content type has elements e.g. accordion, then override this
        method and return 'True'.
        """
        return False

    def set_pending_edit(self):
        """Content has been edited... so update the state.

        If the content was published, then set the state to 'edit'.
        If the content has never been published ('add'), then leave alone.

        """
        if self.is_pending:
            if self.edit_state == EditState._add():
                pass
            elif self.edit_state == EditState._push():
                self.edit_state = EditState._edit()
        else:
            raise BlockError(
                "Sorry, only pending content can be edited."
            )

    def set_pending_pushed(self):
        """Pending content is being 'pushed' ('published')."""
        if self.is_pending:
            self.edit_state = EditState._push()
        else:
            raise BlockError(
                "Sorry, only pending content can be edited."
            )

# -*- encoding: utf-8 -*-
import os
import reversion

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import (
    models,
    transaction,
)
from django.db.models import Max
from django.utils import timezone

from django_extensions.db.fields import AutoSlugField

from base.model_utils import (
    copy_model_instance,
    TimeStampedModel,
)
from base.singleton import SingletonModel


def _default_edit_state():
    return EditState.objects._add().pk


def _default_moderate_state():
    return ModerateState.objects._pending().pk


class Wizard:

    # 'wizard_type'
    IMAGE = 'image'
    LINK = 'link'

    # 'link_type'
    MULTI = 'multi'
    SINGLE = 'single'

    def __init__(self, field_name, wizard_type, link_type):
        self.field_name = field_name
        self.wizard_type = wizard_type
        self.link_type = link_type

    @property
    def css_class(self):
        result = ''
        if self.wizard_type == self.IMAGE:
            result ='fa fa-image'
        elif self.wizard_type == self.LINK:
            result = 'fa fa-globe'
        else:
            raise BlockError(
                "Unknown wizard type: '{}'".format(self.wizard_type)
            )
        return result

    @property
    def url_name(self):
        result = ''
        if self.wizard_type == self.IMAGE:
            result = 'block.wizard.image.option'
        elif self.wizard_type == self.LINK:
            result = 'block.wizard.link.option'
        else:
            raise BlockError(
                "Unknown wizard type: '{}'".format(self.wizard_type)
            )
        return result


class BlockError(Exception):

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr('%s, %s' % (self.__class__.__name__, self.value))


class EditStateManager(models.Manager):

    def _add(self):
        """Internal use only."""
        return EditState.objects.get(slug=EditState.ADD)

    def _edit(self):
        """Internal use only."""
        return EditState.objects.get(slug=EditState.EDIT)

    def _push(self):
        """Internal use only."""
        return EditState.objects.get(slug=EditState.PUSH)

    def create_edit_state(self, slug, name):
        obj = self.model(slug=slug, name=name)
        obj.save()
        return obj


class EditState(models.Model):
    """Add, pushed or editing."""

    ADD = 'add'
    EDIT = 'edit'
    PUSH = 'push'

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    objects = EditStateManager()

    class Meta:
        ordering = ['name']
        verbose_name = 'Edit state'
        verbose_name_plural = 'Edit state'

    def __str__(self):
        return '{}'.format(self.name)

reversion.register(EditState)


class ModerateStateManager(models.Manager):

    def _published(self):
        """Internal use only."""
        return self.model.objects.get(slug=ModerateState.PUBLISHED)

    def _pending(self):
        """Internal use only."""
        return self.model.objects.get(slug=ModerateState.PENDING)

    def _removed(self):
        """Internal use only."""
        return self.model.objects.get(slug=ModerateState.REMOVED)

    def create_moderate_state(self, slug, name):
        obj = self.model(slug=slug, name=name)
        obj.save()
        return obj


class ModerateState(models.Model):
    """Accept, remove or pending."""

    PENDING = 'pending'
    PUBLISHED = 'published'
    REMOVED = 'removed'

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    objects = ModerateStateManager()

    class Meta:
        ordering = ['name']
        verbose_name = 'Moderate'
        verbose_name_plural = 'Moderated'

    def __str__(self):
        return '{}'.format(self.name)

reversion.register(ModerateState)


class PageManager(models.Manager):

    def create_page(
            self, slug_page, slug_menu, name, order, template_name, **kwargs):
        obj = self.model(
            name=name,
            slug=slug_page,
            slug_menu=slug_menu,
            order=order,
            template_name=template_name,
            is_custom=kwargs.get('is_custom', False),
            is_home=kwargs.get('is_home', False),
        )
        obj.save()
        return obj

    def init_page(
            self, slug_page, slug_menu, name, order, template_name, **kwargs):
        if not slug_menu:
            slug_menu = ''
        try:
            obj = Page.objects.get(slug=slug_page, slug_menu=slug_menu)
            obj.name = name
            obj.slug = slug_page
            obj.slug_menu = slug_menu
            obj.order = order
            obj.template_name = template_name
            obj.is_custom = kwargs.get('is_custom', False)
            obj.is_home = kwargs.get('is_home', False)
            obj.save()
        except self.model.DoesNotExist:
            obj = self.create_page(
                slug_page,
                slug_menu,
                name,
                order,
                template_name,
                **kwargs
            )
        return obj

    def menu(self):
        """Return page objects for a menu."""
        return self.pages().exclude(order=0)

    def page_list(self):
        return self.model.objects.all().exclude(
            deleted=True,
        ).order_by(
            'order'
        )

    def pages(self):
        """Return all pages (excluding deleted)."""
        return self.page_list().exclude(
            is_custom=True,
        )


class Page(TimeStampedModel):
    """A page on the web site.

    slug_menu

      The 'slug_menu' is a extra field that can be used to add a page to a
      sub-menu e.g. 'training/faq'.  In this example, the 'slug_menu' would be
      set to 'faq'.

    order

      An order of zero (0) indicates that the page should be excluded from a
      menu - see 'PageManager', 'menu' (although it doesn't look like it
      excludes items with an order of zero!).

    custom

      A custom page is one where the URL and view have been overridden.  This
      is commonly used to add a form to the page, or add extra context.  Our
      convention is to set the 'slug' to 'Page.CUSTOM' for custom pages.

    """
    CUSTOM = 'custom'
    HOME = 'home'

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    slug_menu = models.SlugField(max_length=100, blank=True)
    order = models.IntegerField(default=0)
    is_home = models.BooleanField(default=False)
    template_name = models.CharField(max_length=150)
    deleted = models.BooleanField(default=False)
    is_custom = models.BooleanField(default=False)
    objects = PageManager()

    class Meta:
        ordering = ['order', 'slug', 'slug_menu']
        unique_together = ('slug', 'slug_menu')
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        name = self.url_name
        if self.is_home:
            return reverse(name)
        else:
            return reverse(name, kwargs=self.get_url_kwargs())

    def get_design_url(self):
        return reverse('project.page.design', kwargs=self.get_url_kwargs())

    def get_url_kwargs(self):
        result = dict(page=self.slug,)
        if self.slug_menu:
            result.update(dict(menu=self.slug_menu,))
        return result

    @property
    def url_name(self):
        """Use by this class and the ``Url`` class (see below)."""
        if self.is_home:
            return 'project.home'
        else:
            return 'project.page'

reversion.register(Page)


class PaginatedSection(models.Model):
    """Parameters for a Paginated Section."""

    items_per_page = models.IntegerField(default=10)
    order_by_field = models.CharField(max_length=100)

    def __str__(self):
      return '{} - {}'.format(self.items_per_page, self.order_by_field)

reversion.register(PaginatedSection)


class SectionManager(models.Manager):

    def create_section(
            self, slug, name, block_app, block_model, create_url_name, **kwargs):
        obj = self.model(
            slug=slug,
            name=name,
            block_app=block_app,
            block_model=block_model,
            create_url_name=create_url_name,
        )
        paginated = kwargs.get('paginated', None)
        if paginated:
            obj.paginated = paginated
        obj.save()
        return obj

    def init_section(
            self, slug, name, block_app, block_model, create_url_name, **kwargs):
        """Create a section if it doesn't already exist."""
        if not create_url_name:
            create_url_name = ''
        try:
            obj = Section.objects.get(slug=slug)
            obj.slug = slug
            obj.name = name
            obj.block_app = block_app
            obj.block_model = block_model
            obj.create_url_name = create_url_name
            obj.paginated = kwargs.get('paginated', None)
            obj.save()
        except self.model.DoesNotExist:
            obj = Section.objects.create_section(
                slug,
                name,
                block_app,
                block_model,
                create_url_name,
                **kwargs
            )
        return obj


class Section(TimeStampedModel):
    """Section of the page e.g. content, header, footer."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    block_app = models.CharField(
        max_length=100, help_text="app name e.g. 'compose'"
    )
    block_model = models.CharField(
        max_length=100, help_text="model name e.g. 'Article'"
    )
    create_url_name = models.CharField(
        max_length=100, blank=True,
        help_text="url name for creating the model e.g. 'compose.article.create'"
    )
    paginated = models.ForeignKey(PaginatedSection, blank=True, null=True)
    objects = SectionManager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

    def __str__(self):
        return '{}'.format(self.name)

    def create_url(self, page):
        url = None
        if self.create_url_name:
            kwargs = dict(section=self.slug)
            kwargs.update(page.get_url_kwargs())
            url = reverse(self.create_url_name, kwargs=kwargs)
        return url

reversion.register(Section)


class PageSectionManager(models.Manager):

    def create_page_section(self, page, section):
        obj = self.model(page=page, section=section)
        obj.save()
        return obj

    def init_page_section(self, page, section):
        try:
            obj = PageSection.objects.get(page=page, section=section)
        except self.model.DoesNotExist:
            obj = self.create_page_section(page, section)
        return obj


class PageSection(models.Model):
    """Section of a page."""

    page = models.ForeignKey(Page)
    section = models.ForeignKey(Section)
    objects = PageSectionManager()

    class Meta:
        ordering = ('page__slug', 'section__slug')
        unique_together = ('page', 'section')
        verbose_name = 'Page section'
        verbose_name_plural = 'Page sections'

    def __str__(self):
        return '{} {}'.format(self.page.name, self.section.name)

reversion.register(PageSection)


class BlockModel(TimeStampedModel):
    """Abstract base class for blocks of one type."""

    page_section = models.ForeignKey(PageSection)

    class Meta:
        abstract = True
        verbose_name = 'Block'
        verbose_name_plural = 'Blocks'

    def __str__(self):
        return '{}: page {}, section {}'.format(
            self.pk,
            self.page_section.page.name,
            self.page_section.section.name,
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
            moderate_state=ModerateState.objects._removed()
        )

    def _remove_published_content(self, user):
        """publishing new content, so remove currently published content."""
        try:
            c = self.get_published()
            c._set_moderated(user, ModerateState.objects._removed())
            c.save()
        except ObjectDoesNotExist:
            pass

    def get_pending(self):
        """If the block has pending content, then get it."""
        return self.content.get(
            moderate_state=ModerateState.objects._pending()
        )

    def get_published(self):
        """If the block has published content, then get it."""
        return self.content.get(
            moderate_state=ModerateState.objects._published()
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
            published_instance._set_moderated(
                user, ModerateState.objects._published()
            )
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
                published._set_moderated(
                    user, ModerateState.objects._removed()
                )
                published.save()
                if pending:
                    pending.delete()
            else:
                pending._set_moderated(
                    user, ModerateState.objects._removed()
                )
                pending.save()


class ContentManager(models.Manager):

    def next_order(self):
        result = self.model.objects.aggregate(max_order=Max('order'))
        max_order = result.get('max_order', 0)
        if max_order:
            return max_order + 1
        else:
            return 1

    def pending(self, page_section, kwargs=None):
        """Return a list of pending content for a section.

        Note: we return a list of content instances not a queryset.

        """
        pending = ModerateState.objects._pending()
        qs = self.model.objects.filter(
            block__page_section=page_section,
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

    def published(self, page_section):
        """Return a published content for a page."""
        published = ModerateState.objects._published()
        return self.model.objects.filter(
            block__page_section=page_section,
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
        return self.moderate_state == ModerateState.objects._pending()
    is_pending = property(_is_pending)

    def _is_pending_added(self):
        return self.is_pending and self.edit_state == EditState.objects._add()
    is_pending_added = property(_is_pending_added)

    def _is_pending_edited(self):
        return self.is_pending and self.edit_state == EditState.objects._edit()
    is_pending_edited = property(_is_pending_edited)

    def _is_pending_pushed(self):
        return self.is_pending and self.edit_state == EditState.objects._push()
    is_pending_pushed = property(_is_pending_pushed)

    def _is_published(self):
        return self.moderate_state == ModerateState.objects._published()
    is_published = property(_is_published)

    def _is_removed(self):
        return self.moderate_state == ModerateState.objects._removed()
    is_removed = property(_is_removed)

    def _set_moderated(self, user, moderate_state):
        self.date_moderated = timezone.now()
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
            if self.edit_state == EditState.objects._add():
                pass
            elif self.edit_state == EditState.objects._push():
                self.edit_state = EditState.objects._edit()
        else:
            raise BlockError(
                "Sorry, only pending content can be edited."
            )

    def set_pending_pushed(self):
        """Pending content is being 'pushed' ('published')."""
        if self.is_pending:
            self.edit_state = EditState.objects._push()
        else:
            raise BlockError(
                "Sorry, only pending content can be edited."
            )

    def _wizard_url(self, url_name, field_name, wizard_type):
        content_type = ContentType.objects.get_for_model(self)
        return reverse(
            url_name,
            kwargs={
                'content': content_type.pk,
                'pk': self.pk,
                'field': field_name,
                'type': wizard_type,
            }
        )

    @property
    def wizard_urls(self):
        """Return the URLs for the image and link wizards.

        The return value looks like this::
            [
                {
                    'caption': 'Picture',
                    'url': '/block/wizard/image/29/1/picture/single/',
                    'class': 'fa fa-image'
                },
                {
                    'caption': 'Link',
                    'url': '/block/wizard/link/29/1/link/single/',
                    'class': 'fa fa-globe'
                }
            ]

        """
        result = []
        if hasattr(self, 'wizard_fields'):
            for item in self.wizard_fields:
                result.append({
                    'caption': item.field_name.title(),
                    'class': item.css_class,
                    'url': self._wizard_url(
                        item.url_name,
                        item.field_name,
                        item.link_type,
                    ),
                })
        return result


class Document(models.Model) :

    title = models.CharField(max_length=200)
    document = models.FileField(
        upload_to='link/document',
        blank=True,
        null=True,
        help_text='Uploaded document e.g. PDF'
    )
    original_file_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Original file name of the document'
    )
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        # unique_together = ('page', 'course')
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def save(self, *args, **kwargs):
        """Save the original file name."""
        if self.document.name:
            self.original_file_name = os.path.basename(self.document.name)
        # Call the "real" save() method.
        super().save(*args, **kwargs)

    @property
    def url(self):
        return settings.MEDIA_URL + self.document.name

reversion.register(Document)


class HeaderFooter(SingletonModel):
    """Move to ``block``?"""

    header = models.CharField(max_length=150, blank=True)
    footer_left = models.CharField(max_length=150, blank=True)
    footer_right = models.CharField(max_length=150, blank=True)
    url_twitter = models.URLField(verbose_name='Twitter URL', blank=True)
    url_linkedin = models.URLField(verbose_name='LinkedIn URL', blank=True)
    url_facebook = models.URLField(verbose_name='Facebook URL', blank=True)

    class Meta:
        verbose_name = 'Header and footer'
        verbose_name_plural = 'Header and footers'

    def __str__(self):
        return '{}'.format(self.header)

reversion.register(HeaderFooter)


class ImageCategoryManager(models.Manager):

    def create_category(self, name):
        obj = self.model(name=name)
        obj.save()
        return obj

    def categories(self):
        return self.model.objects.all().exclude(
            deleted=True,
        ).order_by(
            'slug',
        )

    def init_category(self, name):
        count = self.model.objects.filter(name=name).count()
        if not count:
            self.create_category(name)


class ImageCategory(models.Model):

    name = models.CharField(max_length=100)
    slug = AutoSlugField(max_length=100, unique=True, populate_from=('name',))
    deleted = models.BooleanField(default=False)
    objects = ImageCategoryManager()

    class Meta:
        ordering = ['name']
        verbose_name = 'Image Category'
        verbose_name_plural = 'Image Categories'

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def in_use(self):
        images = Image.objects.filter(category=self, deleted=False)
        return images.count() > 0

reversion.register(ImageCategory)


class ImageManager(models.Manager):

    def images(self):
        return self.model.objects.all().exclude(
            deleted=True,
        ).order_by(
            'category__slug',
            'title',
        )


class Image(TimeStampedModel):
    """An image *library*, used with the 'ImageWizard'.

    For more information, see ``1011-generic-carousel/wip.rst``

    .. note:: Images are NOT links... so we don't use the ``LinkWizard``.
              We need a new wizard for images.

    .. note:: Image wizard...  For now... display all the images as little
              thumbnails with tick boxes for multi-selection and radio buttons
              for single selection.

    TODO

    - Do we want to add tags field in here so we can search/group images?
      e.g. https://github.com/alex/django-taggit
    - For now, we are adding a category only.

    """

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='link/image')
    original_file_name = models.CharField(max_length=100)
    deleted = models.BooleanField(default=False)
    category = models.ForeignKey(ImageCategory, blank=True, null=True)
    objects = ImageManager()

    class Meta:
        verbose_name = 'Link Image'
        verbose_name_plural = 'Link Images'

    def __str__(self):
        return '{}'.format(self.title)

    def save(self, *args, **kwargs):
        """Save the original file name."""
        self.original_file_name = os.path.basename(self.image.name)
        # Call the "real" save() method.
        super().save(*args, **kwargs)

    def set_deleted(self):
        self.deleted = True
        self.save()

reversion.register(Image)


class LinkCategoryManager(models.Manager):

    def create_category(self, name):
        obj = self.model(name=name)
        obj.save()
        return obj

    def categories(self):
        return self.model.objects.all().exclude(
            deleted=True,
        ).order_by(
            'slug',
        )

    def init_category(self, name):
        count = self.model.objects.filter(name=name).count()
        if not count:
            self.create_category(name)


class LinkCategory(models.Model):

    name = models.CharField(max_length=100)
    slug = AutoSlugField(max_length=100, unique=True, populate_from=('name',))
    deleted = models.BooleanField(default=False)
    objects = LinkCategoryManager()

    class Meta:
        ordering = ['name']
        verbose_name = 'Link Category'
        verbose_name_plural = 'Link Categories'

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def in_use(self):
        links = Link.objects.filter(category=self, deleted=False)
        return links.count() > 0

reversion.register(LinkCategory)


class UrlManager(models.Manager):

    def init_page_url(self, page):
        if page.is_custom or page.slug == Page.CUSTOM:
            raise BlockError(
                "Cannot create a URL for a custom "
                "page: '{}'".format(page.name)
            )
        if page.deleted:
            raise BlockError(
                "Cannot create a URL for a deleted "
                "page: '{}'".format(page.name)
            )
        try:
            obj = self.model.objects.get(page=page)
            obj.title = page.name
        except self.model.DoesNotExist:
            obj = self.model(
                title=page.name,
                url_type=self.model.PAGE,
                page=page,
            )
        obj.save()
        return obj

    def init_reverse_url(self, title, name, arg1=None, arg2=None, arg3=None):
        arg1 = arg1 or ''
        arg2 = arg2 or ''
        arg3 = arg3 or ''
        try:
            obj = self.model.objects.get(
                name=name,
                arg1=arg1,
                arg2=arg2,
                arg3=arg3,
            )
            obj.title = title
        except self.model.DoesNotExist:
            obj = self.model(
                title=title,
                url_type=self.model.REVERSE,
                name=name,
                arg1=arg1,
                arg2=arg2,
                arg3=arg3,
            )
        # check this is a valid url
        obj.url
        obj.save()
        return obj

    def init_pages(self):
        """Add all non-custom pages to the list of URLs."""
        for page in Page.objects.pages():
            self.init_page_url(page)

    def urls(self):
        return self.model.objects.all().exclude(
            deleted=True,
        ).order_by(
            'title'
        )


class Url(models.Model):
    """List of URLs in this project.

    This is a combination of ``Page`` URLs and view URLs e.g.
    ``block.page.list``.

    In future, we could add the class name of a view to this table and remove
    ``slug`` and ``slug_menu`` from the ``Page`` model.  Malcolm has some ideas
    for this.

    """

    PAGE = 'p'
    REVERSE = 'r'

    URL_TYPE_CHOICES = (
        (PAGE, 'Page'),
        (REVERSE, 'Reverse'),
    )

    title = models.CharField(max_length=200)
    url_type = models.CharField(max_length=1, choices=URL_TYPE_CHOICES)
    page = models.ForeignKey(
        Page,
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=100,
        help_text="e.g. 'project.page' or 'web.training.application'"
    )
    arg1 = models.SlugField(max_length=100, help_text="e.g. 'training'")
    arg2 = models.SlugField(max_length=100, help_text="e.g. 'application'")
    arg3 = models.SlugField(max_length=100, help_text="e.g. 'urgent'")
    deleted = models.BooleanField(default=False)
    objects = UrlManager()

    class Meta:
        unique_together = ('page', 'name', 'arg1', 'arg2', 'arg3')
        verbose_name = 'URL'
        verbose_name_plural = 'URLs'

    def __str__(self):
        return '{}'.format(self.title)

    @property
    def url(self):
        result = None
        if self.url_type == self.PAGE:
            return self.page.get_absolute_url()
        else:
            params = []
            if self.arg1:
                params.append(self.arg1)
            if self.arg2:
                params.append(self.arg2)
            if self.arg3:
                params.append(self.arg3)
            result = reverse(self.name, args=params)
        return result

reversion.register(Url)


class LinkManager(models.Manager):

    def create_document_link(self, document, category=None):
        obj = self.model(
            document=document,
            link_type=self.model.DOCUMENT,
            title=document.title,
        )
        if category:
            obj.category = category
        obj.save()
        return obj

    def create_internal_link(self, url_internal):
        obj = self.model(
            url_internal=url_internal,
            link_type=self.model.URL_INTERNAL,
            title=url_internal.title,
        )
        obj.save()
        return obj

    def links(self):
        """List of links."""
        return self.model.objects.all().exclude(
            deleted=True,
        ).order_by(
            'category__slug',
            'title',
        )


class Link(TimeStampedModel):
    """A link to something.

    Either:

    - document
    - external url
    - internal url

    For more information, see ``1011-generic-carousel/wip.rst``

    TODO

    - Do we want to add tags field in here so we can search/group links?
      e.g. https://github.com/alex/django-taggit

    """

    DOCUMENT = 'd'
    URL_INTERNAL = 'r'
    URL_EXTERNAL = 'u'

    LINK_TYPE_CHOICES = (
        (DOCUMENT, 'Document'),
        (URL_EXTERNAL, 'External URL'),
        (URL_INTERNAL, 'Internal URL'),
    )

    title = models.CharField(max_length=250)
    link_type = models.CharField(max_length=1, choices=LINK_TYPE_CHOICES)
    category = models.ForeignKey(LinkCategory, blank=True, null=True)
    deleted = models.BooleanField(default=False)

    document = models.ForeignKey(
        Document,
        blank=True,
        null=True,
    )
    url_external = models.URLField(
        max_length=512,
        verbose_name='Link',
        blank=True,
        null=True,
        help_text='URL for a web site e.g. http://www.bbc.co.uk/news'
    )
    url_internal = models.ForeignKey(
        Url,
        blank=True,
        null=True,
        help_text='A page on this web site'
    )
    objects = LinkManager()

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

    def __str__(self):
        return '{}'.format(self.title)

    def save(self, *args, **kwargs):
        if self.link_type:
            # Call the "real" save() method.
            super().save(*args, **kwargs)
        else:
            raise BlockError("'Link' records must have a 'link_type'")

    @property
    def file_name(self):
        result = None
        if self.link_type == self.DOCUMENT:
            return self.document.original_file_name
        return result

    @property
    def is_document(self):
        return bool(self.link_type == self.DOCUMENT)

    @property
    def link_type_description(self):
        if self.link_type == self.DOCUMENT:
            return 'Document'
        elif self.link_type == self.URL_EXTERNAL:
            return 'Web Site'
        elif self.link_type == self.URL_INTERNAL:
            return 'Page'
        else:
            raise BlockError(
                "'Link' {} does not have a 'link_type' (or is an "
                "unknown link type: '{}')".format(self.pk, self.link_type)
            )

    @property
    def url(self):
        result = None
        if self.link_type == self.DOCUMENT:
            return self.document.url
        elif self.link_type == self.URL_EXTERNAL:
            return self.url_external
        elif self.link_type == self.URL_INTERNAL:
            return self.url_internal.url
        else:
            raise BlockError(
                "'Link' {} does not have a 'link_type' (or is an "
                "unknown link type: '{}')".format(self.pk, self.link_type)
            )
        return result

reversion.register(Link)


class TemplateManager(models.Manager):
    """Move to ``block``?"""

    def create_template(self, template_name):
        template = self.model(template_name=template_name)
        template.save()
        return template

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

    def __str__(self):
        return '{}'.format(self.title)

    def init_template(self, template_name):
        templates = self.model.objects.filter(template_name=template_name)
        if templates:
            result = templates[0]
        else:
            result = self.create_template(template_name)
        return result


class Template(TimeStampedModel):
    """Move to ``block``?"""

    template_name = models.CharField(
        max_length=150,
        help_text="File name e.g. 'compose/page_article.html'",
    )
    objects = TemplateManager()

    class Meta:
        ordering = ('template_name',)
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'

    def __str__(self):
        return '{}'.format(self.template_name)

    def update_page(self, page):
        # iterate through existing sections in the page
        section_slugs = [s.section.slug for s in page.pagesection_set.all()]
        for slug in section_slugs:
            try:
                # if the section is still used on the page, then keep it.
                template_section = self.templatesection_set.get(
                    section__slug=slug
                )
            except TemplateSection.DoesNotExist:
                # if the section is not used on the page, then delete it.
                PageSection.objects.get(page=page, section__slug=slug).delete()
        # iterate through the new sections
        for template_section in self.templatesection_set.all():
            try:
                # if the section exists on the page, then keep it.
                PageSection.objects.get(
                    page=page, section=template_section.section
                )
            except PageSection.DoesNotExist:
                # if the section is not on the page, then add it.
                page_section = PageSection(
                    page=page,
                    section=template_section.section,
                )
                page_section.save()
        # update the page template name (if it has changed)
        if page.template_name == self.template_name:
            pass
        else:
            page.template_name = self.template_name
            page.save()

    def update_pages(self):
        for p in Page.objects.filter(template_name=self.template_name):
            self.update_page(p)

reversion.register(Template)


class TemplateSectionManager(models.Manager):
    """Move to ``block``?"""

    def create_template_section(self, template, section):
        template_section = self.model(template=template, section=section)
        template_section.save()
        return template_section

    def init_template_section(self, template, section):
        try:
            template_section = self.model.objects.get(
                template=template,
                section=section,
            )
        except self.model.DoesNotExist:
            template_section = self.create_template_section(template, section)
        return template_section


class TemplateSection(TimeStampedModel):
    """Move to ``block``?"""

    template = models.ForeignKey(Template)
    section = models.ForeignKey(Section)
    objects = TemplateSectionManager()

    class Meta:
        ordering = ('template__template_name', 'section__name')
        unique_together = ('template', 'section')
        verbose_name = 'Template section'
        verbose_name_plural = 'Template sections'

    def __str__(self):
        return '{}, {}'.format(self.template.template_name, self.section.name)

reversion.register(TemplateSection)


class ViewUrlManager(models.Manager):

    def create_view_url(self, user, page, url):
        obj = self.model(user=user, page=page, url=url)
        obj.save()
        return obj

    def view_url(self, user, page, url):
        """Get the view URL for a user and page.

        The view URL is the URL we return to when leaving design mode.

        If we don't pass in a URL, but a URL has already been saved for this
        page, then return it.

        """
        url = url or ''
        if page.is_custom:
            try:
                obj = self.model.objects.get(user=user, page=page)
                if url:
                    obj.url = url
                    obj.save()
                else:
                    url = obj.url
            except self.model.DoesNotExist:
                self.create_view_url(user, page, url)
        else:
            url = page.get_absolute_url()
        return url


class ViewUrl(models.Model):
    """Store the view URL for a custom page."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    page = models.ForeignKey(Page)
    url = models.CharField(max_length=200, blank=True)
    objects = ViewUrlManager()

    class Meta:
        ordering = ('user__username', 'page__slug', 'page__slug_menu')
        unique_together = ('user', 'page')
        verbose_name = 'View URL'
        verbose_name_plural = 'View URLs'

    def __str__(self):
        return '{} {}'.format(self.user.username, self.page.name, self.url)

reversion.register(ViewUrl)


class Menu (models.Model):
    slug = models.SlugField(max_length=100)
    title = models.CharField(max_length=100)
    navigation = models.BooleanField(default=True)

    class Meta:
        ordering = ('navigation', 'slug',)
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    def __str__(self):
        return '{}'.format(self.title)

reversion.register(Menu)


class MenuItem (models.Model):
    menu = models.ForeignKey(Menu, blank=False, null=True)
    slug = models.SlugField(max_length=100)
    parent = models.ForeignKey('self', blank=True, null=True)
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    link = models.ForeignKey (Link, blank=True, null=True)

    class Meta:
        ordering=('order','title',)
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return '{} - {}'.format(self.menu.title, self.title)

    def has_children(self):
        return bool(self.menuitem_set.count())

    def has_link(self):
        return bool(self.link)

    def get_link(self):
        if self.link:
            return self.link.url
        else:
            return '#'

reversion.register(MenuItem)

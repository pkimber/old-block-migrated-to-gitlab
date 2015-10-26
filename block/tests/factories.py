# -*- encoding: utf-8 -*-
import factory

from block.models import (
    Document,
    EditState,
    Image,
    ImageCategory,
    Link,
    LinkCategory,
    ModerateState,
    Page,
    PageSection,
    Section,
    Template,
    TemplateSection,
    Url,
)


class DocumentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Document

    document = factory.django.FileField()


class EditStateFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = EditState


class ImageCategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ImageCategory

    @factory.sequence
    def name(n):
        return 'name_{}'.format(n)


class ImageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Image

    image = factory.django.ImageField()


class LinkCategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = LinkCategory

    @factory.sequence
    def name(n):
        return 'name_{}'.format(n)


class LinkFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Link

    link_type = Link.URL_EXTERNAL


class ModerateStateFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ModerateState


class PageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Page

    @factory.sequence
    def order(n):
        """Order '0' excludes from the menu - so include by default."""
        return n + 1

    @factory.sequence
    def slug(n):
        return 'page_{:02d}'.format(n)

    @factory.sequence
    def slug_menu(n):
        return 'menu_{:02d}'.format(n)

    @factory.sequence
    def template_name(n):
        return 'example/template_{:02d}.html'.format(n)


class SectionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Section

    @factory.sequence
    def slug(n):
        return 'slug_{}'.format(n)


class PageSectionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = PageSection

    page = factory.SubFactory(PageFactory)
    section = factory.SubFactory(SectionFactory)


class TemplateFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Template


class TemplateSectionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = TemplateSection

    template = factory.SubFactory(TemplateFactory)
    section = factory.SubFactory(SectionFactory)


class UrlFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Url

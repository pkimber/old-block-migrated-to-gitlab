# -*- encoding: utf-8 -*-
from django.apps import apps
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator,
)
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Max
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.views.generic.base import RedirectView
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
    TemplateView,
)

from block.tasks import thumbnail_image
from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
    SuperuserRequiredMixin,
)
from base.view_utils import BaseMixin, RedirectNextMixin
from .forms import (
    DocumentForm,
    EmptyContentForm,
    EmptyForm,
    ExternalLinkForm,
    HeaderFooterForm,
    ImageCategoryEmptyForm,
    ImageCategoryForm,
    ImageForm,
    ImageListDeleteForm,
    ImageListForm,
    ImageMultiSelectForm,
    ImageSelectForm,
    ImageUpdateForm,
    LinkCategoryEmptyForm,
    LinkCategoryForm,
    LinkEmptyForm,
    LinkListForm,
    LinkMultiSelectForm,
    LinkSelectForm,
    MenuItemEmptyForm,
    MenuItemForm,
    PageEmptyForm,
    PageForm,
    PageFormSimple,
    PageFormSimpleUpdate,
    PageListForm,
    SectionForm,
    TemplateForm,
    TemplateSectionEmptyForm,
    TemplateSectionForm,
)
from .models import (
    BlockError,
    HeaderFooter,
    Image,
    ImageCategory,
    Link,
    LinkCategory,
    Menu,
    MenuItem,
    Page,
    PageSection,
    Section,
    Template,
    TemplateSection,
    Url,
    ViewUrl,
    Wizard,
)


def _get_block_model(page_section):
    block_model = apps.get_model(
        page_section.section.block_app,
        page_section.section.block_model,
    )
    if not block_model:
        raise BlockError("Block model '{}.{}' does not exist.".format(
            page_section.section.block_app,
            page_section.section.block_model,
        ))
    return block_model


def _paginate_section(qs, page_no, section):
    """Paginate the 'block_list' queryset, using page section properties."""
    if section.paginated:
        # this is the block that requires pagination
        if section.paginated.order_by_field:
            qs = qs.order_by(section.paginated.order_by_field)
        if section.paginated.items_per_page:
            paginator = Paginator(qs, section.paginated.items_per_page)
        try:
            qs = paginator.page(page_no)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            qs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            qs = paginator.page(paginator.num_pages)
    return qs


class ContentPageMixin(BaseMixin):
    """Page information."""

    def get_context_data(self, **kwargs):
        context = super(ContentPageMixin, self).get_context_data(**kwargs)
        context.update(dict(
            page=self.get_page(),
            menu_list=Page.objects.menu(),
            footer=self.get_footer(),
        ))
        return context

    def get_footer(self):
        try:
            return Page.objects.get(slug=Page.CUSTOM, slug_menu=Page.FOOTER)
        except Page.DoesNotExist:
            return None

    def get_page(self):
        result = None
        menu = self.kwargs.get('menu', '')
        page = self.kwargs.get('page', '')
        if not page:
            raise BlockError("no 'page' parameter in url")
        try:
            result = Page.objects.get(slug=page, slug_menu=menu)
            if result.deleted:
                raise Http404(
                    "Page '{}', menu '{}' is deleted".format(page, menu)
                )
        except Page.DoesNotExist:
            raise Http404(
                "Page '{}', menu '{}' does not exist".format(page, menu)
            )
        return result

    def get_page_section(self):
        page = self.get_page()
        section = self.get_section()
        try:
            return PageSection.objects.get(page=page, section=section)
        except PageSection.DoesNotExist:
            raise BlockError(
                "Page section '{}/{}' does not exist".format(
                    page.slug,
                    section.slug,
                )
            )

    def get_section(self):
        section = self.kwargs.get('section', None)
        if not section:
            raise BlockError("no 'section' parameter in url")
        try:
            return Section.objects.get(slug=section)
        except Section.DoesNotExist:
            raise BlockError("Section '{}' does not exist".format(section))

    def get_success_url(self):
        return self.object.block.page_section.page.get_design_url()


class ContentCreateView(
        ContentPageMixin, RedirectNextMixin, BaseMixin, CreateView):

    def get_next_order(self, block):
        return self.model.objects.next_order(block)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            block = self.block_class(page_section=self.get_page_section())
        except AttributeError:
            raise BlockError(
                "You need to add the 'block_class' attribute "
                "to your '{}' class.".format(self.__class__.__name__)
            )
        block.save()
        self.object.block = block
        self.object.order = self.get_next_order(block)
        return super().form_valid(form)

    def get_success_url(self):
        url = self.request.POST.get(REDIRECT_FIELD_NAME)
        if not url:
            url = super().get_success_url()
        return url


class ContentPublishView(RedirectNextMixin, BaseMixin, UpdateView):

    def form_valid(self, form):
        """Publish 'pending' content."""
        self.object = form.save(commit=False)
        self.object.block.publish(self.request.user)
        messages.info(
            self.request,
            "Published block, id {}".format(
                self.object.block.pk,
            )
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        url = self.request.POST.get(REDIRECT_FIELD_NAME)
        if not url:
            return self.object.block.page_section.page.get_design_url()
        return url


class ContentRemoveView(RedirectNextMixin, BaseMixin, UpdateView):

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.block.remove(self.request.user)
        messages.info(
            self.request,
            "Removed block {}".format(
                self.object.block.pk,
            )
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        url = self.request.POST.get(REDIRECT_FIELD_NAME)
        if not url:
            return self.object.block.page_section.page.get_design_url()
        return url


class ContentUpdateView(RedirectNextMixin, BaseMixin, UpdateView):

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_pending_edit()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(
            is_update=True,
        ))
        return context

    def get_section(self):
        return self.object.block.section

    def get_success_url(self):
        url = self.request.POST.get(REDIRECT_FIELD_NAME)
        if not url:
            url = self.object.block.page_section.page.get_design_url()
        return url


class ElementCreateView(BaseMixin, CreateView):
    """Update the parent (content) object so it knows it has been changed."""

    def form_valid(self, form):
        self.object = form.save(commit=False)
        content = self.object.get_parent()
        content.set_pending_edit()
        content.save()
        return super(ElementCreateView, self).form_valid(form)


class ElementDeleteView(BaseMixin, DeleteView):
    """Update the parent (content) object so it knows it has been changed."""

    def delete(self, request, *args, **kwargs):
        with transaction.atomic():
            result = super(ElementDeleteView, self).delete(
                request, *args, **kwargs
            )
            content = self.object.get_parent()
            content.set_pending_edit()
            content.save()
        return result


class ElementUpdateView(BaseMixin, UpdateView):
    """Update the parent (content) object so it knows it has been changed."""

    def form_valid(self, form):
        self.object = form.save(commit=False)
        content = self.object.get_parent()
        content.set_pending_edit()
        content.save()
        return super(ElementUpdateView, self).form_valid(form)


class HeaderFooterUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = HeaderFooterForm
    model = HeaderFooter

    def get_object(self, queryset=None):
        return HeaderFooter.load()

    def get_success_url(self):
        return reverse('block.page.list')


class MenuMixin(object):
    """Menu - CRUD views."""

    def _get_menu(self):
        """Default to menu called 'main' for now."""
        return Menu.objects.get(slug=Menu.NAVIGATION)


class MenuItemCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, MenuMixin, BaseMixin,
        CreateView):

    model = MenuItem

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.menu = self._get_menu()
            self.object.slug = slugify(self.object.title)
            self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(dict(
            menu=self._get_menu(),
        ))
        return context

    def get_form_class(self):
        return MenuItemForm

    def get_success_url(self):
        return reverse('block.menuitem.list', args=[self._get_menu().slug])


class MenuItemDeleteView(
        LoginRequiredMixin, StaffuserRequiredMixin, MenuMixin, BaseMixin,
        UpdateView):

    form_class = MenuItemEmptyForm
    model = MenuItem
    template_name = 'block/menuitem_delete_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_deleted(self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('block.menuitem.list', args=[self._get_menu().slug])


class MenuItemListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = MenuItem
    paginate_by = 15

    def get_queryset(self):
        return MenuItem.objects.filter(
            menu__slug=self.kwargs.get('slug', None)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_slug = self.kwargs.get('slug', None)
        try:
            menu = Menu.objects.get(slug=menu_slug)
        except Menu.DoesNotExist:
            # Create the default navigation menu
            menu = Menu.objects.create_menu(
                slug=menu_slug, title="Navigation Menu"
            )
        context.update(dict(
            menu=menu,
        ))
        return context


class MenuItemUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, MenuMixin, BaseMixin,
        UpdateView):

    model = MenuItem

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_class(self):
        return MenuItemForm

    def get_success_url(self):
        return reverse('block.menuitem.list', args=[self._get_menu().slug])


class PageCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    model = Page

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            if not self.request.user.is_superuser:
                self.object.slug = slugify(self.object.name)
                self.object.order = Page.objects.next_order()
            self.object.save()
            self.object.refresh_sections_from_template()
            Url.objects.init_pages()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_class(self):
        if self.request.user.is_superuser:
            return PageForm
        else:
            return PageFormSimple

    def get_success_url(self):
        return reverse('block.page.list')


class PageDeleteView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = PageEmptyForm
    model = Page
    template_name = 'block/page_delete_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.deleted = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('block.page.list')


class PageListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = Page
    paginate_by = 15

    def get_queryset(self):
        return Page.objects.page_list()


class PageTemplateMixin(object):

    def get_template_names(self):
        page = self.get_page()
        return [page.template.template_name, ]


class PageDesignMixin(object):

    def get_section_queryset(self, page_section, page_number):
        block_model = _get_block_model(page_section)
        qs = _paginate_section(
            block_model.objects.pending(page_section),
            page_number,
            page_section.section
        )
        return qs

    def _create_sections(self, page):
        context = {}
        for e in PageSection.objects.filter(page=page):
            qs = self.get_section_queryset(e, self.request.GET.get('page'))
            context.update({
                '{}_list'.format(e.section.slug): qs,
            })
            create_url = e.section.create_url(page)
            if create_url:
                context.update({
                    '{}_create_url'.format(e.section.slug): create_url,
                })
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_page()
        view_url = ViewUrl.objects.view_url(
            self.request.user, page, self.request.GET.get('view')
        )
        context.update(dict(
            design=True,
            is_block_page=True,
            view_url=view_url,
        ))
        sections = self._create_sections(page)
        context.update(sections)
        # footer page
        footer = self.get_footer()
        if footer:
            sections = self._create_sections(footer)
            context.update(sections)
        return context


class PageDesignView(
        LoginRequiredMixin, StaffuserRequiredMixin,
        PageDesignMixin, PageTemplateMixin, ContentPageMixin, TemplateView):
    pass


class PageMixin(object):

    def _check_url(self, page):
        """Check the page is being accessed using the correct URL.

        For custom pages, we make sure the actual URL is different to the
        page URL (we won't have ``custom`` in the URL).  We make an exception
        to this for the home page.

        """
        if self.request.path == page.get_absolute_url():
            if page.is_custom and not page.is_home:
                raise BlockError(
                    "This is a custom page, so the request path "
                    "should NOT match the absolute url: '{}'".format(
                        self.request.path
                    )
                )
        else:
            if page.is_custom:
                pass
            else:
                raise BlockError(
                    "'request.path' ('{}') does not match the absolute url: "
                    "('{}')".format(self.request.path, page.get_absolute_url())
                )

    def _create_sections(self, page):
        context = {}
        for e in PageSection.objects.filter(page=page):
            block_model = _get_block_model(e)
            qs = _paginate_section(
                block_model.objects.published(e),
                self.request.GET.get('page'),
                e.section
            )
            context.update({
                '{}_list'.format(e.section.slug): qs,
            })
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_page()
        self._check_url(page)
        context.update(dict(
            design=False,
            is_block_page=True,
        ))
        sections = self._create_sections(page)
        context.update(sections)
        # footer page
        footer = self.get_footer()
        if footer:
            sections = self._create_sections(footer)
            context.update(sections)
        return context


class PageFormMixin(PageMixin, PageTemplateMixin, ContentPageMixin):
    pass


class PageDetailView(PageFormMixin, DetailView):
    pass


class PageTemplateView(PageFormMixin, TemplateView):
    pass


class PageUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    model = Page

    def get_form_class(self):
        if self.request.user.is_superuser:
            return PageForm
        else:
            return PageFormSimpleUpdate

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            self.object.refresh_sections_from_template()
            Url.objects.init_pages()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('block.page.list')


class CmsMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(
            header_footer=HeaderFooter.load(),
            main_menu_item_list=Menu.objects.navigation_menu_items()
        ))
        return context


class CmsPageDesignView(CmsMixin, PageDesignView):
    pass


class CmsPageView(CmsMixin, PageTemplateView):
    pass


class SectionCreateView(
        LoginRequiredMixin, SuperuserRequiredMixin, BaseMixin, CreateView):

    form_class = SectionForm
    model = Section

    def get_success_url(self):
        return reverse('block.section.list')


class SectionListView(
        LoginRequiredMixin, SuperuserRequiredMixin, BaseMixin, ListView):

    model = Section
    paginate_by = 15


class SectionUpdateView(
        LoginRequiredMixin, SuperuserRequiredMixin, BaseMixin, UpdateView):

    form_class = SectionForm
    model = Section

    def get_success_url(self):
        return reverse('block.section.list')


class TemplateCreateView(
        LoginRequiredMixin, SuperuserRequiredMixin, BaseMixin, CreateView):

    form_class = TemplateForm
    model = Template

    def get_success_url(self):
        return reverse('block.template.list')


class TemplateListView(
        LoginRequiredMixin, SuperuserRequiredMixin, BaseMixin, ListView):

    model = Template
    paginate_by = 15


class TemplateSectionCreateView(
        LoginRequiredMixin, SuperuserRequiredMixin, BaseMixin, CreateView):

    form_class = TemplateSectionForm
    model = TemplateSection

    def _get_template(self):
        pk = self.kwargs.get('pk', None)
        template = Template.objects.get(pk=pk)
        return template

    def get_context_data(self, **kwargs):
        context = super(
            TemplateSectionCreateView, self
        ).get_context_data(**kwargs)
        context.update(dict(template=self._get_template()))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.template = self._get_template()
        with transaction.atomic():
            self.object = form.save()
            # update all the pages with the new sections
            Page.objects.refresh_sections_from_template(self.object.template)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('block.template.list')


class TemplateSectionRemoveView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = TemplateSectionEmptyForm
    model = TemplateSection
    template_name = 'block/templatesection_remove_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        with transaction.atomic():
            self.object.delete()
            # remove sections from all existing pages
            Page.objects.refresh_sections_from_template(self.object.template)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('block.template.list')


class TemplateUpdateView(
        LoginRequiredMixin, SuperuserRequiredMixin, BaseMixin, UpdateView):

    form_class = TemplateForm
    model = Template

    def get_success_url(self):
        return reverse('block.template.list')


class WizardMixin:

    def _content_obj(self):
        content_type_pk = self.kwargs['content']
        pk = self.kwargs['pk']
        content_type = ContentType.objects.get(pk=content_type_pk)
        content_model = content_type.model_class()
        return content_model.objects.get(pk=pk)

    def _field_name(self):
        return self.kwargs['field']

    def _get_field(self):
        content_obj = self._content_obj()
        field_name = self._link_field_name(content_obj)
        return getattr(content_obj, field_name)

    def _get_many_to_many(self):
        link_type = self._link_type()
        if link_type == Wizard.MULTI:
            content_obj = self._content_obj()
            field = self._get_field()
            return field.through.objects.filter(content=content_obj)
        else:
            raise BlockError(
                "Cannot '_get_many_to_many' for 'link_type': '{}'".format(
                    link_type
                )
            )

    def _kwargs(self):
        content_type_pk = self.kwargs['content']
        wizard_type = self.kwargs['type']
        content_obj = self._content_obj()
        return {
            'content': content_type_pk,
            'pk': content_obj.pk,
            'field': self._field_name(),
            'type': wizard_type,
        }

    def _link_field_name(self, content_obj):
        """Assign the link to the field with this name."""
        field_name = self.kwargs['field']
        if hasattr(content_obj, field_name):
            return field_name
        else:
            raise BlockError(
                "Content object '{}' does not have a field "
                "named '{}'".format(content_obj.__class__.__name__, field_name)
            )

    def _link_type(self):
        """Is this a 'single' or a 'multi' link?"""
        return self.kwargs['type']

    def _page_design_url(self, content_obj):
        try:
            result = content_obj.get_design_url()
        except AttributeError:
            result = content_obj.block.page_section.page.get_design_url()
        return result


class WizardImageMixin(WizardMixin):

    def _get_image(self):
        link_type = self._link_type()
        if link_type == Wizard.SINGLE:
            field = self._get_field()
            return field
        else:
            raise BlockError(
                "Cannot '_get_image' for 'link_type': '{}'".format(link_type)
            )

    def _update_image(self, content_obj, image):
        field_name = self._link_field_name(content_obj)
        link_type = self._link_type()
        if link_type == Wizard.SINGLE:
            setattr(content_obj, field_name, image)
        elif link_type == Wizard.MULTI:
            field = self._get_field()
            class_many_to_many = field.through
            result = class_many_to_many.objects.filter(
                content=content_obj
            ).aggregate(
                Max('order')
            )
            order = result.get('order__max') or 0
            order = order + 1
            obj = class_many_to_many(
                content=content_obj,
                image=image,
                order=order,
            )
            obj.save()
        else:
            raise BlockError("Unknown 'link_type': '{}'".format(link_type))
        content_obj.set_pending_edit()
        content_obj.save()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kwargs = self._kwargs()
        # categories
        categories = []
        for category in ImageCategory.objects.categories():
            kw = kwargs.copy()
            kw.update({'category': category.slug})
            url = reverse('block.wizard.image.choose', kwargs=kw)
            categories.append(dict(name=category.name, url=url))
        content_obj = self._content_obj()
        context.update(dict(
            categories=categories,
            field_name=self._field_name(),
            object=content_obj,
            tags=Image.tags.all(),
            url_page_design=self._page_design_url(content_obj),
            url_choose=reverse('block.wizard.image.choose', kwargs=kwargs),
            url_option=reverse('block.wizard.image.option', kwargs=kwargs),
            url_order=reverse('block.wizard.image.order', kwargs=kwargs),
            url_remove=reverse('block.wizard.image.remove', kwargs=kwargs),
            url_select=reverse('block.wizard.image.select', kwargs=kwargs),
            url_upload=reverse('block.wizard.image.upload', kwargs=kwargs),
        ))
        link_type = self._link_type()
        if link_type == Wizard.SINGLE:
            context.update(dict(image=self._get_image()))
        elif link_type == Wizard.MULTI:
            context.update(dict(many_to_many=self._get_many_to_many()))
        else:
            raise BlockError("Unknown 'link_type': '{}'".format(link_type))
        return context


class WizardLinkMixin(WizardMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kwargs = self._kwargs()
        # categories
        categories = []
        for category in LinkCategory.objects.categories():
            kw = kwargs.copy()
            kw.update({'category': category.slug})
            url = reverse('block.wizard.link.choose', kwargs=kw)
            categories.append(dict(name=category.name, url=url))
        content_obj = self._content_obj()
        context.update(dict(
            categories=categories,
            field_name=self._field_name(),
            object=content_obj,
            url_page_design=self._page_design_url(content_obj),
            url_choose=reverse('block.wizard.link.choose', kwargs=kwargs),
            url_external=reverse('block.wizard.link.external', kwargs=kwargs),
            url_option=reverse('block.wizard.link.option', kwargs=kwargs),
            url_page=reverse('block.wizard.link.page', kwargs=kwargs),
            url_order=reverse('block.wizard.link.order', kwargs=kwargs),
            url_remove=reverse('block.wizard.link.remove', kwargs=kwargs),
            url_select=reverse('block.wizard.link.select', kwargs=kwargs),
            url_upload=reverse('block.wizard.link.upload', kwargs=kwargs),
        ))
        link_type = self._link_type()
        if link_type == Wizard.SINGLE:
            context.update(dict(link=self._get_link()))
        elif link_type == Wizard.MULTI:
            context.update(dict(many_to_many=self._get_many_to_many()))
        else:
            raise BlockError("Unknown 'link_type': '{}'".format(link_type))
        return context

    def _get_link(self):
        link_type = self._link_type()
        if link_type == Wizard.SINGLE:
            field = self._get_field()
            return field
        else:
            raise BlockError(
                "Cannot '_get_link' for 'link_type': '{}'".format(link_type)
            )

    def _update_link(self, content_obj, link):
        field_name = self._link_field_name(content_obj)
        link_type = self._link_type()
        if link_type == Wizard.SINGLE:
            setattr(content_obj, field_name, link)
        elif link_type == Wizard.MULTI:
            field = self._get_field()
            class_many_to_many = field.through
            result = class_many_to_many.objects.filter(
                content=content_obj
            ).aggregate(
                Max('order')
            )
            order = result.get('order__max') or 0
            order = order + 1
            obj = class_many_to_many(
                content=content_obj,
                link=link,
                order=order,
            )
            obj.save()
        else:
            raise BlockError("Unknown 'link_type': '{}'".format(link_type))
        content_obj.set_pending_edit()
        content_obj.save()


class WizardImageChoose(
        LoginRequiredMixin, StaffuserRequiredMixin, WizardImageMixin,
        FormView):

    template_name = 'block/wizard_image_choose.html'

    def _category_slug(self):
        return self.kwargs.get('category')

    def _image_queryset(self):
        category_slug = self._category_slug()
        tag = self._tag()
        qs = Image.objects.images()
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        if tag:

            qs = qs.filter(tags__slug__in=[tag])
        return qs

    def _paginator(self, qs):
        page = self.request.GET.get('page')
        paginator = Paginator(qs, 16)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page_obj = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page_obj = paginator.page(paginator.num_pages)
        return page_obj

    def _tag(self):
        return self.request.GET.get('tag')

    def _update_images_many_to_many(self, images):
        content_obj = self._content_obj()
        field = self._get_field()
        with transaction.atomic():
            field = self._get_field()
            class_many_to_many = field.through
            result = class_many_to_many.objects.filter(
                content=content_obj
            ).aggregate(
                Max('order')
            )
            order = result.get('order__max') or 0
            for image in images:
                order = order + 1
                obj = class_many_to_many(
                    content=content_obj,
                    image=image,
                    order=order,
                )
                obj.save()
            content_obj.set_pending_edit()
            content_obj.save()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = None
        category_slug = self._category_slug()
        if category_slug:
            category = ImageCategory.objects.get(slug=category_slug)
            tags = Image.objects.tags_by_category(category)
        else:
            tags = Image.tags.most_common()
        context.update(dict(
            category=category,
            is_paginated=self.page_obj.has_other_pages(),
            page_obj=self.page_obj,
            tag=self._tag(),
            tags=tags,
        ))
        return context

    def get_form_class(self):
        link_type = self._link_type()
        if link_type == Wizard.SINGLE:
            return ImageListForm
        elif link_type == Wizard.MULTI:
            return ImageMultiSelectForm
        else:
            raise BlockError("Unknown 'link_type': '{}'".format(link_type))

    def get_form_kwargs(self):
        """kwargs that will be passed to the __init__ of your form.

        We only paginate the queryset for the form on a ``GET``.  A ``POST``
        needs access to all images for validation.

        The paginator slices the queryset.  If this queryset is passed to the
        form validation, we get a ``Cannot filter a query once a slice has been
        taken`` error message.  To overcome this we create a new queryset:
        http://stackoverflow.com/questions/3470111/cannot-filter-a-query-once-a-slice-has-been-taken

        """
        kwargs = super().get_form_kwargs()
        qs = self._image_queryset()
        if not self.request.method == 'POST':
            self.page_obj = self._paginator(qs)
            qs = Image.objects.filter(pk__in=self.page_obj.object_list)
        kwargs.update(dict(image_queryset=qs))
        return kwargs

    def form_valid(self, form):
        images = form.cleaned_data['images']
        content_obj = self._content_obj()
        link_type = self._link_type()
        if link_type == Wizard.SINGLE:
            self._update_image(content_obj, images)
            url = self._page_design_url(content_obj)
        elif link_type == Wizard.MULTI:
            self._update_images_many_to_many(images)
            url = reverse('block.wizard.image.option', kwargs=self._kwargs())
        else:
            raise BlockError("Unknown 'link_type': '{}'".format(link_type))
        return HttpResponseRedirect(url)


class WizardImageOption(
        LoginRequiredMixin, StaffuserRequiredMixin, WizardImageMixin,
        TemplateView):

    template_name = 'block/wizard_image_option.html'


class WizardImageOrder(
        LoginRequiredMixin, StaffuserRequiredMixin, WizardImageMixin,
        FormView):
    """PJK"""

    form_class = EmptyForm
    template_name = 'block/wizard_image_order.html'

    def _move_up_down(self, up, down):
        pk = int(up) if up else int(down)
        idx = None
        ordered = []
        many_to_many = self._get_many_to_many()
        for count, item in enumerate(many_to_many):
            if item.pk == pk:
                idx = count
            ordered.append(item.pk)
            count = count + 1
        if idx is None:
            raise BlockError("Cannot find item {} in {}".format(pk, ordered))
        if down:
            if idx == len(ordered) - 1:
                raise BlockError("Cannot move the last item down")
            ordered[idx], ordered[idx+1] = ordered[idx+1], ordered[idx]
        elif up:  # up
            if idx == 0:
                raise BlockError("Cannot move the first item up")
            ordered[idx], ordered[idx-1] = ordered[idx-1], ordered[idx]
        else:
            raise BlockError("No 'up' or 'down' (why?)")
        content_obj = self._content_obj()
        field = self._get_field()
        with transaction.atomic():
            for order, pk in enumerate(ordered, start=1):
                obj = field.through.objects.get(
                    pk=pk,
                    content=content_obj,
                )
                obj.order = order
                obj.save()
            content_obj.set_pending_edit()
            content_obj.save()

    def form_valid(self, form):
        up = self.request.POST.get('up')
        down = self.request.POST.get('down')
        if up or down:
            self._move_up_down(up, down)
        return HttpResponseRedirect(
            reverse('block.wizard.image.order', kwargs=self._kwargs())
        )


class WizardImageRemove(
        LoginRequiredMixin, StaffuserRequiredMixin, WizardImageMixin,
        UpdateView):

    form_class = EmptyContentForm
    template_name = 'block/wizard_image_remove.html'

    def form_valid(self, form):
        """Set the image on the content object to ``None`` (remove it)."""
        content_obj = self._content_obj()
        self._update_image(content_obj, None)
        return HttpResponseRedirect(self._page_design_url(content_obj))

    def get_context_data(self, **kwargs):
        """Return the current image in the context, so we can display it."""
        context = super().get_context_data(**kwargs)
        field_name = self.kwargs['field']
        context.update(dict(
            image=getattr(self.object, field_name),
        ))
        return context

    def get_object(self):
        return self._content_obj()


class WizardImageSelect(
        LoginRequiredMixin, StaffuserRequiredMixin, WizardImageMixin,
        FormView):
    """List the current images in the slideshow and allow the user to remove.

    Allow the user to de-select any of the images.

    """

    form_class = ImageSelectForm
    template_name = 'block/wizard_image_select.html'

    def _update_many_to_many(self, many_to_many):
        content_obj = self._content_obj()
        field = self._get_field()
        with transaction.atomic():
            field = self._get_field()
            field.clear()
            class_many_to_many = field.through
            order = 0
            for item in many_to_many:
                order = order + 1
                obj = class_many_to_many(
                    content=content_obj,
                    image=item.image,
                    order=order,
                )
                obj.save()
            content_obj.set_pending_edit()
            content_obj.save()

    def form_valid(self, form):
        many_to_many = form.cleaned_data['many_to_many']
        self._update_many_to_many(many_to_many)
        return HttpResponseRedirect(
            reverse('block.wizard.image.option', kwargs=self._kwargs())
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(dict(many_to_many=self._get_many_to_many()))
        return kwargs


class WizardImageUpload(
        LoginRequiredMixin, StaffuserRequiredMixin, WizardImageMixin,
        CreateView):

    form_class = ImageForm
    template_name = 'block/wizard_image_upload.html'

    def form_valid(self, form):
        content_obj = self._content_obj()
        with transaction.atomic():
            self.object = form.save()
            self._update_image(content_obj, self.object)
        transaction.on_commit(lambda: thumbnail_image.delay(self.object.pk))
        link_type = self._link_type()
        if link_type == Wizard.SINGLE:
            url = self._page_design_url(content_obj)
        elif link_type == Wizard.MULTI:
            url = reverse('block.wizard.image.option', kwargs=self._kwargs())
        return HttpResponseRedirect(url)


class WizardLinkChoose(
        LoginRequiredMixin, StaffuserRequiredMixin, WizardLinkMixin, FormView):
    """ choose a link from the library """

    template_name = 'block/wizard_link_choose.html'

    def _update_links_many_to_many(self, links):
        content_obj = self._content_obj()
        field = self._get_field()
        with transaction.atomic():
            field = self._get_field()
            class_many_to_many = field.through
            result = class_many_to_many.objects.filter(
                content=content_obj
            ).aggregate(
                Max('order')
            )
            order = result.get('order__max') or 0
            for link in links:
                order = order + 1
                obj = class_many_to_many(
                    content=content_obj,
                    link=link,
                    order=order,
                )
                obj.save()
            content_obj.set_pending_edit()
            content_obj.save()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category')
        category = None
        if category_slug:
            category = LinkCategory.objects.get(slug=category_slug)
        context.update(dict(category=category))
        return context

    def get_form_class(self):
        link_type = self._link_type()
        if link_type == Wizard.SINGLE:
            return LinkListForm
        elif link_type == Wizard.MULTI:
            return LinkMultiSelectForm
        else:
            raise BlockError("Unknown 'link_type': '{}'".format(link_type))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        category_slug = self.kwargs.get('category')
        kwargs.update(dict(category_slug=category_slug))
        return kwargs

    def form_valid(self, form):
        links = form.cleaned_data['links']
        content_obj = self._content_obj()
        link_type = self._link_type()
        if link_type == Wizard.SINGLE:
            self._update_link(content_obj, links)
            url = self._page_design_url(content_obj)
        elif link_type == Wizard.MULTI:
            self._update_links_many_to_many(links)
            url = reverse('block.wizard.link.option', kwargs=self._kwargs())
        else:
            raise BlockError("Unknown 'link_type': '{}'".format(link_type))
        return HttpResponseRedirect(url)


class WizardLinkExternal(
        LoginRequiredMixin, StaffuserRequiredMixin, WizardLinkMixin,
        CreateView):
    """ add a link to a url not on this site """

    form_class = ExternalLinkForm
    template_name = 'block/wizard_link_external.html'

    def form_valid(self, form):
        content_obj = self._content_obj()
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.link_type = Link.URL_EXTERNAL
            self.object.save()
            self._update_link(
                content_obj,
                self.object,
            )
        link_type = self._link_type()
        if link_type == Wizard.SINGLE:
            url = self._page_design_url(content_obj)
        elif link_type == Wizard.MULTI:
            url = reverse('block.wizard.link.option', kwargs=self._kwargs())
        return HttpResponseRedirect(url)


class WizardLinkOption(
        LoginRequiredMixin, StaffuserRequiredMixin, WizardLinkMixin,
        TemplateView):

    template_name = 'block/wizard_link_option.html'


class WizardLinkOrder(
        LoginRequiredMixin, StaffuserRequiredMixin, WizardLinkMixin, FormView):
    """ set the order of multiple links """

    form_class = EmptyForm
    template_name = 'block/wizard_link_order.html'

    def _move_up_down(self, up, down):
        pk = int(up) if up else int(down)
        idx = None
        ordered = []
        many_to_many = self._get_many_to_many()
        for count, item in enumerate(many_to_many):
            if item.pk == pk:
                idx = count
            ordered.append(item.pk)
            count = count + 1
        if idx is None:
            raise BlockError("Cannot find item {} in {}".format(pk, ordered))
        if down:
            if idx == len(ordered) - 1:
                raise BlockError("Cannot move the last item down")
            ordered[idx], ordered[idx+1] = ordered[idx+1], ordered[idx]
        elif up:  # up
            if idx == 0:
                raise BlockError("Cannot move the first item up")
            ordered[idx], ordered[idx-1] = ordered[idx-1], ordered[idx]
        else:
            raise BlockError("No 'up' or 'down' (why?)")
        content_obj = self._content_obj()
        field = self._get_field()
        with transaction.atomic():
            for order, pk in enumerate(ordered, start=1):
                obj = field.through.objects.get(
                    pk=pk,
                    content=content_obj,
                )
                obj.order = order
                obj.save()
            content_obj.set_pending_edit()
            content_obj.save()

    def form_valid(self, form):
        up = self.request.POST.get('up')
        down = self.request.POST.get('down')
        if up or down:
            self._move_up_down(up, down)
        return HttpResponseRedirect(
            reverse('block.wizard.link.order', kwargs=self._kwargs())
        )


class WizardLinkPage(
        LoginRequiredMixin, StaffuserRequiredMixin, WizardLinkMixin,
        CreateView):
    """ add a link to a page from this site """

    form_class = PageListForm
    template_name = 'block/wizard_link_page.html'

    def form_valid(self, form):
        content_obj = self._content_obj()
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.link_type = Link.URL_INTERNAL
            self.object.save()
            self._update_link(
                content_obj,
                self.object,
                # Link.objects.create_internal_link(self.object)
            )
        link_type = self._link_type()
        if link_type == Wizard.SINGLE:
            url = self._page_design_url(content_obj)
        elif link_type == Wizard.MULTI:
            url = reverse('block.wizard.link.option', kwargs=self._kwargs())
        return HttpResponseRedirect(url)


class WizardLinkRemove(
        LoginRequiredMixin, StaffuserRequiredMixin, WizardLinkMixin,
        UpdateView):
    """ remove a link """

    form_class = EmptyContentForm
    template_name = 'block/wizard_link_remove.html'

    def form_valid(self, form):
        """Set the link on the content object to ``None`` (remove it)."""
        content_obj = self._content_obj()
        self._update_link(content_obj, None)
        return HttpResponseRedirect(self._page_design_url(content_obj))

    def get_context_data(self, **kwargs):
        """Return the current image in the context, so we can display it."""
        context = super().get_context_data(**kwargs)
        field_name = self.kwargs['field']
        context.update(dict(
            link=getattr(self.object, field_name),
        ))
        return context

    def get_object(self):
        return self._content_obj()


class WizardLinkUpload(
        LoginRequiredMixin, StaffuserRequiredMixin, WizardLinkMixin,
        CreateView):
    """ Upload a document and link to it """

    form_class = DocumentForm
    template_name = 'block/wizard_link_upload.html'

    def form_valid(self, form):
        category = form.cleaned_data['category']
        content_obj = self._content_obj()
        with transaction.atomic():
            self.object = form.save()
            self._update_link(
                content_obj,
                Link.objects.create_document_link(self.object, category)
            )
        link_type = self._link_type()
        if link_type == Wizard.SINGLE:
            url = self._page_design_url(content_obj)
        elif link_type == Wizard.MULTI:
            url = reverse('block.wizard.link.option', kwargs=self._kwargs())
        return HttpResponseRedirect(url)


class ImageListView(LoginRequiredMixin, StaffuserRequiredMixin, ListView):

    def get_queryset(self):
        return Image.objects.images()


class ImageListDeleteView(
        LoginRequiredMixin, StaffuserRequiredMixin, FormView):
    """Mark images (in the library) as deleted.

    Images will still be attached to content objects, but will not display in
    the library (image wizard).

    """

    form_class = ImageListDeleteForm
    template_name = 'block/image_list_delete.html'

    def form_valid(self, form):
        images = form.cleaned_data['images']
        for image in images:
            image.set_deleted()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('block.image.list')


class ImageUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, UpdateView):

    form_class = ImageUpdateForm
    model = Image

    def get_success_url(self):
        return reverse('block.image.list')


class ImageCategoryCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = ImageCategoryForm
    model = ImageCategory

    def get_success_url(self):
        return reverse('block.image.category.list')


class ImageCategoryDeleteView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = ImageCategoryEmptyForm
    model = ImageCategory
    template_name = 'block/imagecategory_delete_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.in_use:
            raise BlockError(
                "Cannot delete an image category which is "
                "in use: '{}'".format(self.object.slug)
            )
        self.object.deleted = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('block.image.category.list')


class ImageCategoryListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = ImageCategory

    def get_queryset(self):
        return ImageCategory.objects.categories()


class ImageCategoryUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = ImageCategoryForm
    model = ImageCategory

    def get_success_url(self):
        return reverse('block.image.category.list')


class LinkCategoryCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = LinkCategoryForm
    model = LinkCategory

    def get_success_url(self):
        return reverse('block.link.category.list')


class LinkCategoryDeleteView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = LinkCategoryEmptyForm
    model = LinkCategory
    template_name = 'block/linkcategory_delete_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.in_use:
            raise BlockError(
                "Cannot delete a link category which is "
                "in use: '{}'".format(self.object.slug)
            )
        self.object.deleted = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('block.link.category.list')


class LinkCategoryListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = LinkCategory

    def get_queryset(self):
        return LinkCategory.objects.categories()


class LinkCategoryUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = LinkCategoryForm
    model = LinkCategory

    def get_success_url(self):
        return reverse('block.link.category.list')


class LinkListView(LoginRequiredMixin, StaffuserRequiredMixin, ListView):

    def get_queryset(self):
        return Link.objects.links()


class LinkUpdateMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'url_option': reverse('block.link.list')})
        return context


class LinkDocumentCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, LinkUpdateMixin,
        CreateView):
    """ Upload a document and link to it """

    form_class = DocumentForm
    template_name = 'block/wizard_link_upload.html'

    def form_valid(self, form):
        category = form.cleaned_data['category']
        with transaction.atomic():
            self.object = form.save()
            Link.objects.create_document_link(self.object, category)
        url = reverse('block.link.list')
        return HttpResponseRedirect(url)


class LinkDocumentUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, LinkUpdateMixin,
        UpdateView):

    """ Update a document link

    N.B. A bit more complicated because we need to reference the Link in the
    in the url to the this view but to manage uploading the file the form's
    model is Document
    """
    form_class = DocumentForm
    template_name = 'block/wizard_link_upload.html'

    @property
    def _link(self):
        return Link.objects.get(pk=self.kwargs.get('pk'))

    def get_object(self):
        return self._link.document

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'in_library': True})
        return kwargs

    def form_valid(self, form):
        category = form.cleaned_data['category']
        with transaction.atomic():
            self.object = form.save()
            link = self._link
            link.title = self.object.title
            link.category = category
            link.save()
        return HttpResponseRedirect(reverse('block.link.list'))

    def get_initial(self):
        return {'category': self._link.category}

    def get_success_url(self):
        return reverse('block.link.list')


class LinkUrlExternalUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, LinkUpdateMixin,
        UpdateView):
    """ add a link to a url not on this site """

    form_class = ExternalLinkForm
    template_name = 'block/wizard_link_external.html'
    model = Link

    def get_success_url(self):
        return reverse('block.link.list')


class LinkUrlInternalUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, LinkUpdateMixin,
        UpdateView):

    """ update a link to a page from this site """

    form_class = PageListForm
    template_name = 'block/wizard_link_page.html'
    model = Link

    def get_success_url(self):
        return reverse('block.link.list')


class LinkDeleteView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = LinkEmptyForm
    model = Link
    template_name = 'block/link_delete_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.in_use:
            raise BlockError(
                "Cannot delete a link which is "
                "in use: '{}'".format(self.object.title)
            )
        self.object.deleted = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('block.link.list')


class LinkRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.get('pk')
        type = kwargs.get('type')
        link = Link.objects.get(pk=pk)
        link = get_object_or_404(Link, pk=pk, link_type=type)
        self.url = link.url
        return super().get_redirect_url(*args, **kwargs)


class WizardLinkSelect(
        LoginRequiredMixin, StaffuserRequiredMixin, WizardLinkMixin, FormView):
    """List the current links in the slideshow and allow the user to remove.

    Allow the user to de-select any of the images.

    """

    form_class = LinkSelectForm
    template_name = 'block/wizard_link_select.html'

    def _update_many_to_many(self, many_to_many):
        content_obj = self._content_obj()
        field = self._get_field()
        with transaction.atomic():
            field = self._get_field()
            field.clear()
            class_many_to_many = field.through
            order = 0
            for item in many_to_many:
                order = order + 1
                obj = class_many_to_many(
                    content=content_obj,
                    link=item.link,
                    order=order,
                )
                obj.save()
            content_obj.set_pending_edit()
            content_obj.save()

    def form_valid(self, form):
        many_to_many = form.cleaned_data['many_to_many']
        self._update_many_to_many(many_to_many)
        return HttpResponseRedirect(
            reverse('block.wizard.link.option', kwargs=self._kwargs())
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(dict(many_to_many=self._get_many_to_many()))
        return kwargs

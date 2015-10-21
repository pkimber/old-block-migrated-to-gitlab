# -*- encoding: utf-8 -*-
import os

from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import FileSystemStorage
from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator,
)
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import (
    get_model,
    Max,
)
from django.http import HttpResponseRedirect
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
    TemplateView,
)

from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
    SuperuserRequiredMixin,
)
from formtools.wizard.views import SessionWizardView

from base.view_utils import BaseMixin
from .forms import (
    DocumentForm,
    DocumentListForm,
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
    ImageTypeForm,
    ImageUpdateForm,
    LinkMultiSelectForm,
    LinkTypeForm,
    PageEmptyForm,
    PageForm,
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
    Menu,
    MenuItem,
    Page,
    PageSection,
    Section,
    Template,
    TemplateSection,
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
            # If page is out of range (e.g. 9999), deliver last page of results.
            qs = paginator.page(paginator.num_pages)
    return qs


class ContentPageMixin(BaseMixin):
    """Page information."""

    def get_context_data(self, **kwargs):
        context = super(ContentPageMixin, self).get_context_data(**kwargs)
        context.update(dict(
            page=self.get_page(),
            menu_list=Page.objects.menu(),
        ))
        return context

    def get_page(self):
        menu = self.kwargs.get('menu', None)
        page = self.kwargs.get('page', None)
        if not page:
            raise BlockError("no 'page' parameter in url")
        try:
            if menu:
                return Page.objects.get(slug=page, slug_menu=menu)
            else:
                return Page.objects.get(slug=page, slug_menu='')
        except Page.DoesNotExist:
            raise BlockError(
                "Page '{}', menu '{}' does not exist".format(page, menu)
            )

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


class ContentCreateView(ContentPageMixin, BaseMixin, CreateView):

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
        self.object.order = self.model.objects.next_order()
        return super(ContentCreateView, self).form_valid(form)


class ContentPublishView(BaseMixin, UpdateView):

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
        return self.object.block.page_section.page.get_design_url()


class ContentRemoveView(BaseMixin, UpdateView):

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
        return self.object.block.page_section.page.get_design_url()


class ContentUpdateView(BaseMixin, UpdateView):

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_pending_edit()
        return super(ContentUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ContentUpdateView, self).get_context_data(**kwargs)
        context.update(dict(
            is_update=True,
        ))
        return context

    def get_section(self):
        return self.object.block.section

    def get_success_url(self):
        return self.object.block.page_section.page.get_design_url()


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


class PageCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = PageForm
    model = Page

    def form_valid(self, form):
        template = form.cleaned_data.get('template')
        with transaction.atomic():
            self.object = form.save()
            template.update_page(self.object)
        return HttpResponseRedirect(self.get_success_url())

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

    def get_template_names(self) :
        page = self.get_page()
        if page.template_name:
            template_name = page.template_name
        else:
            raise BlockError(
                "Page '{}' has no 'template_name'".format(page.slug)
            )
        return [template_name,]


class PageDesignMixin(object):

    def get_context_data(self, **kwargs):
        context = super(PageDesignMixin, self).get_context_data(**kwargs)
        page = self.get_page()
        view_url = ViewUrl.objects.view_url(
            self.request.user, page, self.request.GET.get('view')
        )
        context.update(dict(
            design=True,
            is_block_page=True,
            view_url=view_url,
        ))
        for e in PageSection.objects.filter(page=page) :
            block_model = _get_block_model(e)
            qs = _paginate_section(
                block_model.objects.pending(e),
                self.request.GET.get('page'),
                e.section
            )
            context.update({
                '{}_list'.format(e.section.slug): qs,
            })
            create_url = e.section.create_url(page)
            if create_url:
                context.update({
                    '{}_create_url'.format(e.section.slug): create_url,
                })
        return context


class PageDesignView(
        LoginRequiredMixin, StaffuserRequiredMixin,
        PageDesignMixin, PageTemplateMixin, ContentPageMixin, TemplateView):
    pass


class PageMixin(object):

    def _check_url(self, page):
        """Check the page is being accessed using the correct URL."""
        if self.request.path == page.get_absolute_url():
            if page.is_custom:
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

    def get_context_data(self, **kwargs):
        context = super(PageMixin, self).get_context_data(**kwargs)
        page = self.get_page()
        self._check_url(page)
        context.update(dict(
            design=False,
            is_block_page=True,
        ))
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


class PageFormMixin(PageMixin, PageTemplateMixin, ContentPageMixin):
    pass


class PageDetailView(PageFormMixin, DetailView):
    pass


class PageTemplateView(PageFormMixin, TemplateView):
    pass


class PageUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = PageForm
    model = Page

    def get_initial(self):
        """Returns the initial data to use for forms on this view."""
        try:
            template = Template.objects.get(
                template_name=self.object.template_name
            )
            return dict(template=template)
        except Template.DoesNotExist:
            return dict()

    def form_valid(self, form):
        template = form.cleaned_data.get('template')
        with transaction.atomic():
            self.object = form.save()
            template.update_page(self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('block.page.list')


class CmsMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            main_menu_items = MenuItem.objects.filter(
                menu__slug='main',
                parent=None
            )
        except MenuItem.DoesNotExist:
            main_menu_items = []
        context.update(dict(
            header_footer=HeaderFooter.load(),
            main_menu_items=main_menu_items
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
            self.object.template.update_pages()
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
            self.object.template.update_pages()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('block.template.list')


class TemplateUpdateView(
        LoginRequiredMixin, SuperuserRequiredMixin, BaseMixin, UpdateView):

    form_class = TemplateForm
    model = Template

    def get_success_url(self):
        return reverse('block.template.list')


# -----------------------------------------------------------------------------
# LinkWizard

def select_link_form(wizard, link_type) :
    """Return true if user has selected 'link_type'."""
    data = wizard.get_cleaned_data_for_step(LinkTypeForm.FORM_LINK_TYPE)
    selected = data['link_type'] if data else None
    return selected == link_type


def url_existing(wizard):
    """Return true if user opts for existing document link"""
    return select_link_form(wizard, LinkTypeForm.FORM_DOCUMENT_LIST)


def url_existing_link_multi(wizard):
    """Return true if user opts for an existing link."""
    return select_link_form(wizard, LinkTypeForm.FORM_LINK_MULTI_REMOVE)


def url_external_link(wizard):
    """Return true if user opts for external link """
    return select_link_form(wizard, LinkTypeForm.FORM_EXTERNAL_URL)


def url_internal_page(wizard):
    """Return true if user opts for an internal page """
    return select_link_form(wizard, LinkTypeForm.FORM_PAGE_URL)


def url_upload(wizard):
    """Return true if user opts for upload a document """
    return select_link_form(wizard, LinkTypeForm.FORM_DOCUMENT)


class LinkWizard(LoginRequiredMixin, StaffuserRequiredMixin, SessionWizardView):
    """Link Wizard.

    The link wizard will allow the user to:

    1) Enter or edit an external URL e.g. http://www.bbc.co.uk/news
    2) Select an internal URL for a page on this web site.
    3) Select a document, or create a new document.

    Documentation for the SessionWizardView in
    http://django-formtools.readthedocs.org/en/latest/

    """

    condition_dict = {
        LinkTypeForm.FORM_EXTERNAL_URL: url_external_link,
        LinkTypeForm.FORM_PAGE_URL: url_internal_page,
        LinkTypeForm.FORM_DOCUMENT: url_upload,
        LinkTypeForm.FORM_DOCUMENT_LIST: url_existing,
        LinkTypeForm.FORM_LINK_MULTI_REMOVE: url_existing_link_multi,
    }

    temp_dir = 'temp'
    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, 'temp/wizard')
    )
    # this list of forms must stay in this order!
    form_list = [
        (LinkTypeForm.FORM_LINK_TYPE, LinkTypeForm),
        (LinkTypeForm.FORM_EXTERNAL_URL, ExternalLinkForm),
        (LinkTypeForm.FORM_PAGE_URL, PageListForm),
        (LinkTypeForm.FORM_DOCUMENT, DocumentForm),
        (LinkTypeForm.FORM_DOCUMENT_LIST, DocumentListForm),
        (LinkTypeForm.FORM_LINK_MULTI_REMOVE, LinkMultiSelectForm),
    ]

    form_link_type_map = {
        LinkTypeForm.FORM_DOCUMENT: Link.DOCUMENT,
        LinkTypeForm.FORM_DOCUMENT_LIST: Link.DOCUMENT,
        LinkTypeForm.FORM_EXTERNAL_URL: Link.URL_EXTERNAL,
        LinkTypeForm.FORM_PAGE_URL: Link.URL_INTERNAL,
    }
    template_name = 'block/wizard.html'

    def _get_current_content_instance(self):
        content_pk = self.kwargs['content']
        pk = self.kwargs['pk']
        content_type = ContentType.objects.get(pk=content_pk)
        content_model = content_type.model_class()
        return content_model.objects.get(pk=pk)

    def _get_link_field_name(self, content_obj):
        """Assign the link to the field with this name."""
        return self.kwargs['field']

    def _get_link_type(self):
        """Is this a 'single' or a 'multi' link?"""
        return self.kwargs['type']

    def _save_link(self, form, content_obj, link_type):
        link = form.save(commit=False)
        link.link_type = link_type
        link = form.save()
        self._update_link(content_obj, link)

    def _update_link(self, content_obj, link):
        field_name = self._get_link_field_name(content_obj)
        link_type = self._get_link_type()
        if link_type == Wizard.SINGLE:
            if not hasattr(content_obj, field_name):
                raise BlockError(
                    "Content object '{}' does not have a field "
                    "named '{}'".format(content_obj.__class__.__name__, field_name)
                )
            setattr(content_obj, field_name, link)
        elif link_type == Wizard.MULTI:
            field = getattr(content_obj, field_name)
            field.add(link)

    def _update_links(self, content_obj, links):
        field_name = self._get_link_field_name(content_obj)
        field = getattr(content_obj, field_name)
        field.clear()
        for link in links:
            field.add(link)

    def get_form_kwargs(self, step):
        result = {}
        link_type = self._get_link_type()
        if step == LinkTypeForm.FORM_LINK_TYPE:
            result.update({
                'link_type': link_type,
            })
        elif step == LinkTypeForm.FORM_LINK_MULTI_REMOVE:
            # list the current links for the content object
            content_obj = self._get_current_content_instance()
            field_name = self._get_link_field_name(content_obj)
            field = getattr(content_obj, field_name)
            result.update({
                'links': field.all(),
            })
        return result

    def done(self, form_list, form_dict, **kwargs):
        form_link_type = form_dict[LinkTypeForm.FORM_LINK_TYPE]
        form_id = form_link_type.cleaned_data['link_type']
        with transaction.atomic():
            obj = self._get_current_content_instance()
            if form_id == LinkTypeForm.REMOVE:
                self._update_link(obj, None)
            elif form_id == LinkTypeForm.FORM_LINK_MULTI_REMOVE:
                form = form_dict[form_id]
                links = form.cleaned_data['links']
                self._update_links(obj, links)
            else:
                form = form_dict[form_id]
                if form_id == LinkTypeForm.FORM_DOCUMENT:
                    form = form_dict[form_id]
                    document = form.save()
                    self._update_link(obj, Link.objects.create_document_link(document))
                else:
                    link_type = self.form_link_type_map[form_id]
                    self._save_link(form, obj, link_type)
            obj.set_pending_edit()
            obj.save()

        try:
            url = obj.get_design_url()
        except:
            url = obj.block.page_section.page.get_design_url()
        return HttpResponseRedirect(url)


class WizardMixin:

    def _content_obj(self):
        content_type_pk = self.kwargs['content']
        pk = self.kwargs['pk']
        content_type = ContentType.objects.get(pk=content_type_pk)
        content_model = content_type.model_class()
        return content_model.objects.get(pk=pk)

    def _field_name(self):
        return self.kwargs['field']

    def _get_field(self): #, content_obj):
        content_obj = self._content_obj()
        field_name = self._link_field_name(content_obj)
        return getattr(content_obj, field_name)

    def _get_many_to_many(self):
        link_type = self._link_type()
        if link_type == Wizard.MULTI:
            content_obj = self._content_obj()
            #import pdb; pdb.set_trace()
            #print(content_obj)
            #return content_obj.many_to_many()
            field = self._get_field()
            return field.through.objects.filter(content_obj=content_obj)
        else:
            raise BlockError(
                "Cannot '_get_many_to_many' for 'link_type': '{}'".format(
                    link_type
                )
            )

    def _get_image(self):
        #result = []
        link_type = self._link_type()
        if link_type == Wizard.SINGLE:
            field = self._get_field()
            return field
            #result.append(field)
        else:
            raise BlockError(
                "Cannot '_get_image' for 'link_type': '{}'".format(link_type)
            )
        #elif link_type == Wizard.MULTI:
        #    for image in field.all():
        #        result.append(image)
        #return result

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
        return content_obj.block.page_section.page.get_design_url()

    def _update_image(self, content_obj, image):
        field_name = self._link_field_name(content_obj)
        link_type = self._link_type()
        if link_type == Wizard.SINGLE:
            setattr(content_obj, field_name, image)
        elif link_type == Wizard.MULTI:
            field = self._get_field()
            class_many_to_many = field.through
            result = class_many_to_many.objects.filter(
                content_obj=content_obj
            ).aggregate(
                Max('order')
            )
            order = result.get('order__max', 1) + 1
            obj = class_many_to_many(
                content_obj=content_obj,
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
            #link_type=self._link_type(),
            object=content_obj,
            url_page_design=self._page_design_url(content_obj),
            url_choose=reverse('block.wizard.image.choose', kwargs=kwargs),
            url_option=reverse('block.wizard.image.option', kwargs=kwargs),
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


class WizardImageChoose(
        LoginRequiredMixin, StaffuserRequiredMixin, WizardMixin, FormView):

    form_class = ImageListForm
    template_name = 'block/wizard_image_choose.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category')
        category = None
        if category_slug:
            category = ImageCategory.objects.get(slug=category_slug)
        context.update(dict(category=category))
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        category_slug = self.kwargs.get('category')
        kwargs.update(dict(category_slug=category_slug))
        return kwargs

    def form_valid(self, form):
        image = form.cleaned_data['images']
        content_obj = self._content_obj()
        self._update_image(content_obj, image)
        link_type = self._link_type()
        if link_type == Wizard.SINGLE:
            url = self._page_design_url(content_obj)
        elif link_type == Wizard.MULTI:
            url = reverse('block.wizard.image.option', kwargs=self._kwargs())
        return HttpResponseRedirect(url)


class WizardImageOption(
        LoginRequiredMixin, StaffuserRequiredMixin, WizardMixin, TemplateView):

    template_name = 'block/wizard_image_option.html'


class WizardImageRemove(
        LoginRequiredMixin, StaffuserRequiredMixin, WizardMixin, UpdateView):

    form_class = EmptyForm
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
        LoginRequiredMixin, StaffuserRequiredMixin, WizardMixin, FormView):
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
                    content_obj=content_obj,
                    image=item.image,
                    order=order,
                )
                obj.save()

    def form_valid(self, form):
        content_obj = self._content_obj()
        many_to_many = form.cleaned_data['many_to_many']
        self._update_many_to_many(many_to_many)
        return HttpResponseRedirect(
            reverse('block.wizard.image.option', kwargs=self._kwargs())
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(dict(many_to_many=self._get_many_to_many()))
        return kwargs

    def get_object(self):
        return self._content_obj()


class WizardImageUpload(
        LoginRequiredMixin, StaffuserRequiredMixin, WizardMixin, CreateView):

    form_class = ImageForm
    template_name = 'block/wizard_image_upload.html'

    def form_valid(self, form):
        content_obj = self._content_obj()
        with transaction.atomic():
            self.object = form.save()
            self._update_image(content_obj, self.object)
        link_type = self._link_type()
        if link_type == Wizard.SINGLE:
            url = self._page_design_url(content_obj)
        elif link_type == Wizard.MULTI:
            url = reverse('block.wizard.image.option', kwargs=self._kwargs())
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


class ImageCategoryUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = ImageCategoryForm
    model = ImageCategory

    def get_success_url(self):
        return reverse('block.image.category.list')

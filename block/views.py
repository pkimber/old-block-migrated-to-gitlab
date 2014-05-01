# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import get_model
from django.http import HttpResponseRedirect
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    TemplateView,
)

from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
)

from base.view_utils import BaseMixin

from .models import (
    BlockError,
    Page,
    PageSection,
    Section,
)


def get_block_model(page_section):
    block_model = get_model(
        page_section.section.block_app,
        page_section.section.block_model,
    )
    if not block_model:
        raise BlockError("Block model '{}.{}' does not exist.".format(
            page_section.section.block_app,
            page_section.section.block_model,
        ))
    return block_model


class ContentPageMixin(BaseMixin):
    """Page information."""

    def get_context_data(self, **kwargs):
        context = super(ContentPageMixin, self).get_context_data(**kwargs)
        context.update(dict(
            page=self.get_page(),
            pages=Page.objects.menu(),
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


class PageListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = Page
    paginate_by = 15

    def get_queryset(self):
        return Page.objects.all().order_by('name')


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
        context.update(dict(
            design=True,
            is_block_page=True,
        ))
        for e in PageSection.objects.filter(page=page) :
            block_create_url = '{}_create_url'.format(e.section.slug)
            block_list_name = '{}_list'.format(e.section.slug)
            block_model = get_block_model(e)
            block_list = block_model.objects.pending(e)
            try:
                if (e.section.paginated):
                    # this is the block that requires pagination
                    if (e.section.paginated.order_by_field != None):
                        all_objects = block_list.order_by(e.section.paginated.order_by_field)
                    else:
                        all_objects = block_list

                    if (e.section.paginated.items_per_page):
                        paginator = Paginator(all_objects,
                            e.section.paginated.items_per_page)
                    pageNo = self.request.GET.get('page')
                    try:
                        block_list = paginator.page(pageNo)
                    except PageNotAnInteger:
                        # If page is not an integer, deliver first page.
                        block_list = paginator.page(1)
                    except EmptyPage:
                        # If page is out of range (e.g. 9999), deliver last page of results.
                        block_list = paginator.page(paginator.num_pages)
            except:
                pass

            kwargs = dict(section=e.section.slug)
            kwargs.update(page.get_url_kwargs())
            context.update({
                block_list_name: block_list,
            })
            if e.section.create_url_name:
                context.update({
                    block_create_url: reverse(
                        e.section.create_url_name, kwargs=kwargs
                    ),
                })
        return context


class PageDesignView(
        LoginRequiredMixin, StaffuserRequiredMixin,
        PageDesignMixin, PageTemplateMixin, ContentPageMixin, TemplateView):

    pass


class PageMixin(object):

    def get_context_data(self, **kwargs):
        context = super(PageMixin, self).get_context_data(**kwargs)
        page = self.get_page()
        context.update(dict(
            design=False,
            is_block_page=True,
        ))
        for e in PageSection.objects.filter(page=page):
            block_list_name = '{}_list'.format(e.section.slug)
            block_model = get_block_model(e)
            block_list = block_model.objects.published(e)
            try:
                if (e.section.paginated):
                    # this is the block that requires pagination
                    if (e.section.paginated.order_by_field != None):
                        all_objects = block_list.order_by(e.section.paginated.order_by_field)
                    else:
                        all_objects = block_list

                    if (e.section.paginated.items_per_page):
                        paginator = Paginator(all_objects,
                            e.section.paginated.items_per_page)
                    pageNo = self.request.GET.get('page')
                    try:
                        block_list = paginator.page(pageNo)
                    except PageNotAnInteger:
                        # If page is not an integer, deliver first page.
                        block_list = paginator.page(1)
                    except EmptyPage:
                        # If page is out of range (e.g. 9999), deliver last page of results.
                        block_list = paginator.page(paginator.num_pages)
            except:
                pass

            context.update({
                block_list_name: block_list,
            })
        return context


class PageView(
        PageMixin, PageTemplateMixin, ContentPageMixin, TemplateView):

    pass


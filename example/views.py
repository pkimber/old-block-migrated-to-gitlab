# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView

from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
)

from block.tests.scenario import get_section_body
from block.views import (
    ContentCreateView,
    ContentPageMixin,
    ContentPublishView,
    ContentRemoveView,
    ContentUpdateView,
)

from .forms import (
    TitleEmptyForm,
    TitleForm,
)
from .models import (
    Title,
    TitleBlock,
)


class HomeView(TemplateView):

    template_name = 'example/home.html'


class PageBaseView(ContentPageMixin, TemplateView):

    template_name = 'example/page_content.html'

    def _get_body(self):
        return get_section_body()


class PageDesignView(LoginRequiredMixin, StaffuserRequiredMixin, PageBaseView):

    def get_context_data(self, **kwargs):
        context = super(PageDesignView, self).get_context_data(**kwargs)
        content = Title.objects.pending(
            self.get_page(),
            self._get_body()
        )
        context.update(dict(
            design=True,
            content=content,
        ))
        return context


class PageView(PageBaseView):

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)
        content = Title.objects.published(
            self.get_page(),
            self._get_body()
        )
        context.update(dict(
            design=False,
            content=content,
        ))
        return context


class TitleCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, ContentCreateView):

    block_class = TitleBlock
    form_class = TitleForm
    model = Title
    template_name = 'example/title_update.html'


class TitleUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, ContentUpdateView):

    form_class = TitleForm
    model = Title
    template_name = 'example/title_update.html'


class TitlePublishView(
        LoginRequiredMixin, StaffuserRequiredMixin, ContentPublishView):

    form_class = TitleEmptyForm
    model = Title
    template_name = 'example/title_publish.html'


class TitleRemoveView(
        LoginRequiredMixin, StaffuserRequiredMixin, ContentRemoveView):

    form_class = TitleEmptyForm
    model = Title
    template_name = 'example/title_remove.html'

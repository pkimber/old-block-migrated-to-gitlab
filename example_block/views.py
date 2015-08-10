# -*- encoding: utf-8 -*-
from django.views.generic import (
    ListView,
    TemplateView,
)

from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
)

from base.view_utils import BaseMixin
from block.forms import ContentEmptyForm
from block.models import Page
from block.views import (
    ContentCreateView,
    ContentPublishView,
    ContentRemoveView,
    ContentUpdateView,
    PageView,
)

from .forms import TitleForm
from .models import (
    Title,
    TitleBlock,
)


class ExampleView(PageView):

    def get_context_data(self, **kwargs):
        context = super(ExampleView, self).get_context_data(**kwargs)
        context.update(dict(
            calendar=('Jan', 'Feb', 'Mar'),
        ))
        return context


class SettingsView(BaseMixin, TemplateView):

    template_name = 'example/settings.html'


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

    form_class = ContentEmptyForm
    model = Title
    template_name = 'example/title_publish.html'


class TitleRemoveView(
        LoginRequiredMixin, StaffuserRequiredMixin, ContentRemoveView):

    form_class = ContentEmptyForm
    model = Title
    template_name = 'example/title_remove.html'

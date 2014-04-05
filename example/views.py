# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView

from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
)

from block.forms import ContentEmptyForm
from block.tests.scenario import get_section_body
from block.views import (
    ContentCreateView,
    ContentPageMixin,
    ContentPublishView,
    ContentRemoveView,
    ContentUpdateView,
)

from .forms import TitleForm
from .models import (
    Title,
    TitleBlock,
)


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

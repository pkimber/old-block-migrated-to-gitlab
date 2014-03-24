# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView

from block.tests.scenario import (
    get_page_home,
    get_section_body,
)

from example.models import Title

class HomeView(TemplateView):

    template_name = 'example/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        page = get_page_home()
        section = get_section_body()
        pending = Title.objects.pending(page, section)
        context.update(dict(
            pending=pending,
        ))
        return context

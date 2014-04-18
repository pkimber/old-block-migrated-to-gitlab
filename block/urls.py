# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import (
    patterns, url
)

from .views import PageListView


urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=PageListView.as_view(),
        name='block.page.list'
        ),
)

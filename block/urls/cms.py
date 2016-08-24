# -*- encoding: utf-8 -*-
from django.conf.urls import url

from block.models import Page
from block.views import CmsPageDesignView, CmsPageView


urlpatterns = [
    url(regex=r'^$',
        view=CmsPageView.as_view(),
        kwargs=dict(page=Page.HOME),
        name='project.home'
        ),
    url(regex=r'^(?P<page>[-\w\d]+)/design/$',
        view=CmsPageDesignView.as_view(),
        name='project.page.design'
        ),
    url(regex=r'^(?P<page>[-\w\d]+)/(?P<menu>[-\w\d]+)/design/$',
        view=CmsPageDesignView.as_view(),
        name='project.page.design'
        ),
    url(regex=r'^(?P<page>[-\w\d]+)/$',
        view=CmsPageView.as_view(),
        name='project.page'
        ),
    url(regex=r'^(?P<page>[-\w\d]+)/(?P<menu>[-\w\d]+)/$',
        view=CmsPageView.as_view(),
        name='project.page'
        ),
]

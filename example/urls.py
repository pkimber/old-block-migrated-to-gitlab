# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from .views import (
    HomeView,
    PageDesignView,
    PageView,
    TitleCreateView,
    TitlePublishView,
    TitleRemoveView,
    TitleUpdateView,
)

admin.autodiscover()


urlpatterns = patterns(
    '',

    url(regex=r'^$',
        view=PageView.as_view(),
        kwargs=dict(page='home'),
        name='project.home'
        ),
    url(regex=r'^(?P<page>[-\w\d]+)/$',
        view=PageView.as_view(),
        name='project.page'
        ),
    url(regex=r'^(?P<page>[-\w\d]+)/design/$',
        view=PageDesignView.as_view(),
        name='project.page.design'
        ),

    url(regex=r'^title/create/(?P<page>[-\w\d]+)/(?P<section>[-\w\d]+)/$',
        view=TitleCreateView.as_view(),
        name='example.title.create'
        ),
    url(regex=r'^title/(?P<pk>\d+)/publish/$',
        view=TitlePublishView.as_view(),
        name='example.title.publish'
        ),
    url(regex=r'^title/(?P<pk>\d+)/edit/$',
        view=TitleUpdateView.as_view(),
        name='example.title.update'
        ),
    url(regex=r'^title/(?P<pk>\d+)/remove/$',
        view=TitleRemoveView.as_view(),
        name='example.title.remove'
        ),

    url(regex=r'^admin/',
        view=include(admin.site.urls)
        ),
    url(regex=r'^',
        view=include('login.urls')
        ),
    url(r'^home/user/$',
        view=RedirectView.as_view(url=reverse_lazy('project.home')),
        name='project.home.user'
        ),
)

urlpatterns += staticfiles_urlpatterns()

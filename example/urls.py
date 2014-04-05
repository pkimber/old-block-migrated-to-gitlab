# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from block.views import (
    PageDesignView,
    PageView,
)

from .views import (
    TitleCreateView,
    TitlePublishView,
    TitleRemoveView,
    TitleUpdateView,
)

admin.autodiscover()


urlpatterns = patterns(
    '',
    # '/' send to home
    url(regex=r'^$',
        view=PageView.as_view(),
        kwargs=dict(page='home'),
        name='project.home'
        ),
    # block page view
    url(regex=r'^(?P<page>[-\w\d]+)/$',
        view=PageView.as_view(),
        name='project.page'
        ),
    # block page design
    url(regex=r'^(?P<page>[-\w\d]+)/design/$',
        view=PageDesignView.as_view(),
        name='project.page.design'
        ),
    # title create, publish, update and remove
    url(regex=r'^title/create/(?P<page>[-\w\d]+)/(?P<section>[-\w\d]+)/$',
        view=TitleCreateView.as_view(),
        name='example.title.create'
        ),
    url(regex=r'^title/(?P<pk>\d+)/publish/$',
        view=TitlePublishView.as_view(),
        name='example.title.publish'
        ),
    url(regex=r'^title/(?P<pk>\d+)/update/$',
        view=TitleUpdateView.as_view(),
        name='example.title.update'
        ),
    url(regex=r'^title/(?P<pk>\d+)/remove/$',
        view=TitleRemoveView.as_view(),
        name='example.title.remove'
        ),
    # admin, login
    url(regex=r'^admin/',
        view=include(admin.site.urls)
        ),
    url(regex=r'^',
        view=include('login.urls')
        ),
    # home page when logged in
    url(r'^home/user/$',
        view=RedirectView.as_view(url=reverse_lazy('project.home')),
        name='project.home.user'
        ),
)

urlpatterns += staticfiles_urlpatterns()

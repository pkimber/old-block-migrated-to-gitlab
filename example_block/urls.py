# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from block.models import Page
from block.views import (
    PageDesignView,
    PageView,
)

from .views import (
    ExampleView,
    PageListView,
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
        kwargs=dict(page=Page.HOME),
        name='project.home'
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
        name='project.dash'
        ),
    # custom page - see https://www.pkimber.net/open/app-block.html
    url(regex=r'^calendar/information/$',
        view=ExampleView.as_view(),
        kwargs=dict(page=Page.CUSTOM, menu='calendar-information'),
        name='calendar.information'
        ),
    # list of pages
    url(regex=r'^block/page/list/$',
        view=PageListView.as_view(),
        name='block.page.list'
        ),
    # block page design
    url(regex=r'^(?P<page>[-\w\d]+)/design/$',
        view=PageDesignView.as_view(),
        name='project.page.design'
        ),
    url(regex=r'^(?P<page>[-\w\d]+)/(?P<menu>[-\w\d]+)/design/$',
        view=PageDesignView.as_view(),
        name='project.page.design'
        ),
    # block page view
    url(regex=r'^(?P<page>[-\w\d]+)/$',
        view=PageView.as_view(),
        name='project.page'
        ),
    url(regex=r'^(?P<page>[-\w\d]+)/(?P<menu>[-\w\d]+)/$',
        view=PageView.as_view(),
        name='project.page'
        ),
    # title create, publish, update and remove
    url(regex=r'^title/create/(?P<page>[-\w\d]+)/(?P<section>[-\w\d]+)/$',
        view=TitleCreateView.as_view(),
        name='example.title.create'
        ),
    url(regex=r'^title/create/(?P<page>[-\w\d]+)/(?P<menu>[-\w\d]+)/(?P<section>[-\w\d]+)/$',
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
)

urlpatterns += staticfiles_urlpatterns()

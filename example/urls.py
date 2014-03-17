# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from .views import HomeView

admin.autodiscover()


urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=HomeView.as_view(),
        name='project.home'
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
    # test view - so 'check_content_methods' will pass
    url(regex=r'^example/(?P<pk>\d+)/publish/$',
        view=RedirectView.as_view(url=reverse_lazy('project.home')),
        name='example.test.publish'
        ),
    # test view - so 'check_content_methods' will pass
    url(regex=r'^example/(?P<pk>\d+)/remove/$',
        view=RedirectView.as_view(url=reverse_lazy('project.home')),
        name='example.test.remove'
        ),
    # test view - so 'check_content_methods' will pass
    url(regex=r'^example/(?P<pk>\d+)/update/$',
        view=RedirectView.as_view(url=reverse_lazy('project.home')),
        name='example.test.update'
        ),
)

urlpatterns += staticfiles_urlpatterns()

# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url

#TBUSHELL import the new SiteMap class
from .sitemaps import SiteMapName


from .views import PageListView

#from django.contrib import admin
#admin.autodiscover()

#TBUSHELL sitemap dictionary
#sitemaps = {
#    'default': SiteMapName,
#}


urlpatterns = patterns('',
    #TBUSHELL call the sitemap dictionary
   #url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
   url(
       regex=r'^page/$',
       view=PageListView.as_view(),
       name='block.page.list'
    ),
)


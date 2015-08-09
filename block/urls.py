# -*- encoding: utf-8 -*-
from django.conf.urls import (
    patterns,
    url,
)

from .views import (
    ImageWizard,
    LinkWizard,
)


urlpatterns = patterns(
    '',
    url(regex=r'^wizard/image/(?P<content>\d+)/(?P<pk>\d+)/(?P<field>[-\w\d]+)/$',
        view=ImageWizard.as_view(),
        name='block.image.wizard'
        ),
    url(regex=r'^wizard/link/(?P<content>\d+)/(?P<pk>\d+)/(?P<field>[-\w\d]+)/$',
        view=LinkWizard.as_view(),
        name='block.link.wizard'
        ),
)

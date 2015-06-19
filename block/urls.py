# -*- encoding: utf-8 -*-
from django.conf.urls import (
    patterns,
    url,
)

from .views import LinkWizard


urlpatterns = patterns(
    '',
    url(regex=r'^wizard/(?P<content>\d+)/(?P<pk>\d+)/link/$',
        view=LinkWizard.as_view(),
        name='block.link.wizard'
        ),
)

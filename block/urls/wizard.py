# -*- encoding: utf-8 -*-
from django.conf.urls import (
    patterns,
    url,
)


from block.views import (
    WizardImageChoose,
    WizardImageOption,
    WizardImageOrder,
    WizardImageRemove,
    WizardImageSelect,
    WizardImageUpload,
)


urlpatterns = patterns(
    '',
    url(regex=r'^image/(?P<content>\d+)/(?P<pk>\d+)/(?P<field>[-\w\d]+)/(?P<type>[-\w\d]+)/choose/$',
        view=WizardImageChoose.as_view(),
        name='block.wizard.image.choose'
        ),
    url(regex=r'^image/(?P<content>\d+)/(?P<pk>\d+)/(?P<field>[-\w\d]+)/(?P<type>[-\w\d]+)/(?P<category>[-\w\d]+)/choose/$',
        view=WizardImageChoose.as_view(),
        name='block.wizard.image.choose'
        ),
    url(regex=r'^image/(?P<content>\d+)/(?P<pk>\d+)/(?P<field>[-\w\d]+)/(?P<type>[-\w\d]+)/order/$',
        view=WizardImageOrder.as_view(),
        name='block.wizard.image.order'
        ),
    url(regex=r'^image/(?P<content>\d+)/(?P<pk>\d+)/(?P<field>[-\w\d]+)/(?P<type>[-\w\d]+)/option/$',
        view=WizardImageOption.as_view(),
        name='block.wizard.image.option'
        ),
    url(regex=r'^image/(?P<content>\d+)/(?P<pk>\d+)/(?P<field>[-\w\d]+)/(?P<type>[-\w\d]+)/remove/$',
        view=WizardImageRemove.as_view(),
        name='block.wizard.image.remove'
        ),
    url(regex=r'^image/(?P<content>\d+)/(?P<pk>\d+)/(?P<field>[-\w\d]+)/(?P<type>[-\w\d]+)/select/$',
        view=WizardImageSelect.as_view(),
        name='block.wizard.image.select'
        ),
    url(regex=r'^image/(?P<content>\d+)/(?P<pk>\d+)/(?P<field>[-\w\d]+)/(?P<type>[-\w\d]+)/upload/$',
        view=WizardImageUpload.as_view(),
        name='block.wizard.image.upload'
        ),
    #url(regex=r'^wizard/image/(?P<content>\d+)/(?P<pk>\d+)/(?P<field>[-\w\d]+)/(?P<type>[-\w\d]+)/$',
    #    view=ImageWizard.as_view(),
    #    name='block.image.wizard'
    #    ),
)

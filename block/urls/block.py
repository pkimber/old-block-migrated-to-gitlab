# -*- encoding: utf-8 -*-
from django.conf.urls import (
    patterns,
    url,
)

from block.views import (
    HeaderFooterUpdateView,
    ImageWizard,
    LinkWizard,
    PageCreateView,
    PageDeleteView,
    PageListView,
    PageUpdateView,
    SectionCreateView,
    SectionListView,
    SectionUpdateView,
    TemplateCreateView,
    TemplateListView,
    TemplateSectionCreateView,
    TemplateSectionRemoveView,
    TemplateUpdateView,
    WizardImageOption,
    WizardImageUpload,
)


urlpatterns = patterns(
    '',
    url(regex=r'^header-footer/$',
        view=HeaderFooterUpdateView.as_view(),
        name='block.header.footer.update'
        ),
    url(regex=r'^page/$',
        view=PageListView.as_view(),
        name='block.page.list'
        ),
    url(regex=r'^page/create/$',
        view=PageCreateView.as_view(),
        name='block.page.create'
        ),
    url(regex=r'^page/(?P<pk>\d+)/delete/$',
        view=PageDeleteView.as_view(),
        name='block.page.delete'
        ),
    url(regex=r'^page/(?P<pk>\d+)/update/$',
        view=PageUpdateView.as_view(),
        name='block.page.update'
        ),
    url(regex=r'^section/$',
        view=SectionListView.as_view(),
        name='block.section.list'
        ),
    url(regex=r'^section/create/$',
        view=SectionCreateView.as_view(),
        name='block.section.create'
        ),
    url(regex=r'^section/(?P<pk>\d+)/update/$',
        view=SectionUpdateView.as_view(),
        name='block.section.update'
        ),
    url(regex=r'^template/$',
        view=TemplateListView.as_view(),
        name='block.template.list'
        ),
    url(regex=r'^template/create/$',
        view=TemplateCreateView.as_view(),
        name='block.template.create'
        ),
    url(regex=r'^template/(?P<pk>\d+)/update/$',
        view=TemplateUpdateView.as_view(),
        name='block.template.update'
        ),
    url(regex=r'^template/(?P<pk>\d+)/section/create/$',
        view=TemplateSectionCreateView.as_view(),
        name='block.template.section.create'
        ),
    url(regex=r'^template/section/(?P<pk>\d+)/remove/$',
        view=TemplateSectionRemoveView.as_view(),
        name='block.template.section.remove'
        ),
    url(regex=r'^wizard/image/(?P<content>\d+)/(?P<pk>\d+)/(?P<field>[-\w\d]+)/(?P<type>[-\w\d]+)/option/$',
        view=WizardImageOption.as_view(),
        name='block.wizard.image.option'
        ),
    url(regex=r'^wizard/image/(?P<content>\d+)/(?P<pk>\d+)/(?P<field>[-\w\d]+)/(?P<type>[-\w\d]+)/upload/$',
        view=WizardImageUpload.as_view(),
        name='block.wizard.image.upload'
        ),
    #url(regex=r'^wizard/image/(?P<content>\d+)/(?P<pk>\d+)/(?P<field>[-\w\d]+)/(?P<type>[-\w\d]+)/$',
    #    view=ImageWizard.as_view(),
    #    name='block.image.wizard'
    #    ),
    url(regex=r'^wizard/link/(?P<content>\d+)/(?P<pk>\d+)/(?P<field>[-\w\d]+)/(?P<type>[-\w\d]+)/$',
        view=LinkWizard.as_view(),
        name='block.link.wizard'
        ),
)

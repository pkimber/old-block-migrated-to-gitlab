# -*- encoding: utf-8 -*-
from django import forms

from block.models import (
    ContentModel,
    Document,
    Link,
    Page,
)


class ContentEmptyForm(forms.ModelForm):

    class Meta:
        model = ContentModel
        fields = ()


class DocumentListForm(forms.ModelForm):
    """List of documents (for the form wizard)."""

    def __init__(self, *args, **kwargs):
        super ().__init__(*args,**kwargs)
        for name in ('title', 'document'):
            self.fields[name].widget.attrs.update({'class': 'pure-input-2-3'})

    class Meta:
        model = Link
        fields = (
            'title',
            'document',
        )


class ExternalLinkForm(forms.ModelForm):
    """Enter a URL for a web site (for the form wizard)."""

    def __init__(self, *args, **kwargs):
        super ().__init__(*args,**kwargs)
        for name in ('title', 'url_external'):
            self.fields[name].widget.attrs.update({'class': 'pure-input-2-3'})

    class Meta:
        model = Link
        fields = (
            'title',
            'url_external',
        )


class PageListForm(forms.ModelForm):
    """Select a page from this web site (for the form wizard)."""

    def __init__(self, *args, **kwargs):
        super ().__init__(*args,**kwargs)
        self.fields['title'].widget.attrs.update({'class': 'pure-input-2-3'})
        self.fields['url_internal'].label = 'URL'

    class Meta:
        model = Link
        fields = (
            'title',
            'url_internal',
        )


class LinkTypeForm(forms.Form):
    """Allow the user to select the link type (for the form wizard)."""

    FORM_DOCUMENT = 'u'
    FORM_DOCUMENT_LIST = 'e'
    FORM_EXTERNAL_URL = 'l'
    FORM_PAGE_URL = 'p'
    # this form :)
    FORM_LINK_TYPE = 'link_type'
    # remove does not have a form
    REMOVE = 'r'

    link_type = forms.ChoiceField(
        choices=(
            (FORM_EXTERNAL_URL, 'Link to another site'),
            (FORM_PAGE_URL, 'Page on this site'),
            (FORM_DOCUMENT, 'Upload a document and link to it'),
            (FORM_DOCUMENT_LIST, 'Use an existing document'),
            (REMOVE, 'Remove Link'),
        ),
        label="Choose the type of link",
    )

    class Meta:
        fields = (
            'link_type',
        )


class DocumentForm(forms.ModelForm):
    """Allow the user to upload a document (for the form wizard)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'pure-input-2-3'})

    class Meta:
        model = Document
        fields = (
            'title',
            'document',
        )
        widgets = {
            'document': forms.FileInput,
        }

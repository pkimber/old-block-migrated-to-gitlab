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


class URLExternalLinkForm(forms.ModelForm):

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


class UrlListForm(forms.ModelForm):

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

    FORM_DOCUMENT = 'u'
    FORM_EXISTING = 'e'
    FORM_EXTERNAL_URL = 'l'
    FORM_LINK_TYPE = 'link_type'
    FORM_PAGE = 'p'

    link_type = forms.ChoiceField(
        choices=(
            (FORM_EXTERNAL_URL, 'Link to another site'),
            (FORM_PAGE, 'Page on this site'),
            (FORM_DOCUMENT, 'Upload a document and link to it'),
            (FORM_EXISTING, 'Use an existing document'),
            ('n', 'Remove Link'),
        ),
        label="Choose the type of link",
    )

    class Meta:
        fields = (
            'link_type',
        )


class DocumentForm(forms.ModelForm):
    """Was ``URLUploadForm``."""

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

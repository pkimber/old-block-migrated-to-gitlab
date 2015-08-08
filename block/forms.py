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

    #title = forms.CharField(max_length=512, label="Link Text")
    #url_external = forms.URLField(label="External Link")

    def __init__(self, *args, **kwargs):
        super ().__init__(*args,**kwargs)
        for name in ('title', 'url_external'):
            self.fields[name].widget.attrs.update({'class': 'pure-input-2-3'})
        #if ('use_title' in self.initial and self.initial['use_title'] == False):
        #    self.fields.pop('title')

    class Meta:
        model = Link
        fields = (
            'title',
            'url_external',
        )


#class URLInternalPageForm(forms.Form):
#    title = forms.CharField(max_length=512, label="Link Text")
#
#    def __init__(self, *args, **kwargs):
#        super(URLInternalPageForm, self).__init__(*args, **kwargs)
#        self.fields['url'] = forms.ChoiceField( 
#            choices=[
#                (o.get_absolute_url(), str(o)) for o in Page.objects.all().order_by('name').exclude(deleted=True)
#            ],
#            label="Choose a page"
#        )
#
#        if ('use_title' in self.initial and self.initial['use_title'] == False):
#            self.fields.pop('title')
#
#    class Meta:
#        fields = (
#            'title',
#            'url',
#        )


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

    #EXISTING_DOCUMENT = 'e'
    #PAGE = 'p'
    #UPLOAD = 'u'
    #URL_EXTERNAL = 'l'

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

    #title = forms.CharField(max_length=512, label="Link Text")
    #short_file_name = forms.CharField(
    #    label="Existing Document",
    #    required=False,
    #)
    #document = forms.FileField(
    #    label="Choose a document to upload",
    #    required=True,
    #)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'pure-input-2-3'})
    #    if 'doc_id' in self.initial:
    #        # called from DocumentWizard
    #        self.fields['doc_id'] = forms.CharField(
    #            widget=forms.HiddenInput(),
    #            initial=self.initial['doc_id'],
    #            required=False,
    #            label='',
    #        )
    #        self.fields['short_file_name'].widget.attrs.update({'readonly': True})
    #        self.fields['document'].required = False
    #        self.fields['document'].label="Upload a new document to replace the existing one"
    #    else:
    #        # called from URLChoiceWizard
    #        self.fields.pop('short_file_name')
    #        self.fields['document'].widget.attrs.update({'required': True})


    class Meta:
        model = Document
        fields = (
            'title',
            'document',
        )
        widgets = {
            'document': forms.FileInput,
        }

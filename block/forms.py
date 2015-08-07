# -*- encoding: utf-8 -*-
from django import forms

from block.models import (
    ContentModel,
    Link,
    Page,
)


class ContentEmptyForm(forms.ModelForm):

    class Meta:
        model = ContentModel
        fields = ()


class URLExistingForm(forms.Form):

    title = forms.CharField(max_length=512, label="Link Text")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'] = forms.ChoiceField(
            choices=[
                (o.get_url(), str(o)) for o in LinkDocument.objects.all().order_by('description')
            ],
            label="Choose a Document"
        )
        if ('use_title' in self.initial and self.initial['use_title'] == False):
            self.fields.pop('title')

    class Meta:
        fields = (
            'title',
            'url',
        )


class URLExternalLinkForm(forms.Form):
    title = forms.CharField(max_length=512, label="Link Text")
    url = forms.URLField(label="External Link")

    def __init__(self, *args, **kwargs):
        super (URLExternalLinkForm, self).__init__(*args,**kwargs)

        if ('use_title' in self.initial and self.initial['use_title'] == False):
            self.fields.pop('title')

    class Meta:
        fields = (
            'title',
            'url',
        )


class URLInternalPageForm(forms.Form):
    title = forms.CharField(max_length=512, label="Link Text")

    def __init__(self, *args, **kwargs):
        super(URLInternalPageForm, self).__init__(*args, **kwargs)
        self.fields['url'] = forms.ChoiceField( 
            choices=[
                (o.get_absolute_url(), str(o)) for o in Page.objects.all().order_by('name').exclude(deleted=True)
            ],
            label="Choose a page"
        )

        if ('use_title' in self.initial and self.initial['use_title'] == False):
            self.fields.pop('title')

    class Meta:
        fields = (
            'title',
            'url',
        )


class URLTypeForm(forms.Form):

    UPLOAD = 'u'

    link_type = forms.ChoiceField(
        choices=(
            ('l', 'Link to another site'),
            ('p', 'Page on this site'),
            (UPLOAD, 'Upload a document and link to it'),
            ('e', 'Use an existing document'),
            ('n', 'Remove Link'),
        ),
        label="Choose the type of link",
    )

    class Meta:
        fields = (
            'url_type',
        )


class LinkDocumentForm(forms.ModelForm):
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
        for name in ('title', 'description'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )
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
        model = Link
        fields = (
            'document',
            'title',
            'description',
        )
        widgets = {
            'document': forms.FileInput,
            #'doc_id': forms.HiddenInput(),
        }

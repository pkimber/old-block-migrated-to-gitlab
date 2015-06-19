# -*- encoding: utf-8 -*-
from django import forms

from block.models import (
    ContentModel,
    Page,
)


class ContentEmptyForm(forms.ModelForm):

    class Meta:
        model = ContentModel
        fields = ()


class URLExistingForm(forms.Form):
    title = forms.CharField(max_length=512, label="Link Text")

    def __init__(self, *args, **kwargs):
        super(URLExistingForm, self).__init__(*args, **kwargs)
        self.fields['url'] = forms.ChoiceField( 
            choices=[
                (o.get_url(), str(o)) for o in Document.objects.all().order_by('title')
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

    url_type = forms.ChoiceField(
        choices=(
            ('l', 'Link to another site'),
            ('p', 'Page on this site'),
            ('u', 'Upload a document and link to it'),
            ('e', 'Use an existing document'),
            ('n', 'Remove Link'),
        ),
        label="Choose the type of link",
    )

    class Meta:
        fields = (
            'url_type',
        )


class URLUploadForm(forms.Form):

    title = forms.CharField(max_length=512, label="Link Text")

    short_file_name = forms.CharField(
        label="Existing Document",
        required=False,
    )

    url = forms.FileField(
        label="Choose a document to upload",
        required=True,
    )

    perm_type = forms.ChoiceField(
        choices=(
            ('x', 'Public'),
            ('m', 'Restrict by Membership'),
            ('c', 'Restrict by Course'),
        ),
        label="Choose who has access to this document",
    )


    def __init__(self, *args, **kwargs):
        super(URLUploadForm, self).__init__(*args, **kwargs)

        if 'doc_id' in self.initial:
            # called form DocumentWizard
            self.fields['doc_id'] = forms.CharField(
                widget=forms.HiddenInput(),
                initial=self.initial['doc_id'],
                required=False,
                label='',
            )
            self.fields['short_file_name'].widget.attrs.update({'readonly': True})
            self.fields['url'].required = False
            self.fields['url'].label="Upload a new document to replace the existing one"
        else:
            # called from URLChoiceWizard
            self.fields.pop('short_file_name')
            self.fields['url'].widget.attrs.update({'required': True})


    class Meta:
        fields = (
            'url',
            'title',
            'perm_type',
        )
        widgets = {
            'url': forms.FileInput,
            'doc_id': forms.HiddenInput(),
        }

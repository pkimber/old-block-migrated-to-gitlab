# -*- encoding: utf-8 -*-
from django import forms
from django.conf import settings
from django.forms.widgets import RadioFieldRenderer
from django.utils.html import (
    format_html,
    format_html_join,
)

from easy_thumbnails.files import get_thumbnailer

from block.models import (
    ContentModel,
    Document,
    Image,
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


class ImageForm(forms.ModelForm):
    """Allow the user to upload an image (for the form wizard)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('alt', 'title'):
            self.fields[name].widget.attrs.update({'class': 'pure-input-2-3'})

    class Meta:
        model = Image
        fields = (
            'title',
            'image',
            'alt',
        )
        widgets = {
            'image': forms.FileInput,
        }


class ImageModelChoiceField(forms.ModelChoiceField):
    """The label is the image."""

    def label_from_instance(self, obj):
        thumbnailer = get_thumbnailer(obj.image)
        thumbnail_options = {
            'crop': True,
            'size': (100, 100),
        }
        thumbnail = thumbnailer.get_thumbnail(thumbnail_options)
        return format_html('{}<br /><img src="{}" />'.format(
            obj.title,
            thumbnail.url,
        ))


class RadioRendererNoBullet(RadioFieldRenderer):
    """Render radio buttons without bullet points."""

    def render(self):
        return format_html('\n'.join(['{}\n'.format(w) for w in self]))


class ImageListForm(forms.Form):
    """List of images (for the form wizard)."""

    images = ImageModelChoiceField(
        queryset=Image.objects.all(),
        empty_label=None,
        widget=forms.RadioSelect(renderer=RadioRendererNoBullet),
    )

    class Meta:
        model = Image
        fields = (
            'images',
        )


class ImageTypeForm(forms.Form):
    """Allow the user to select the image type (for the form wizard)."""

    FORM_IMAGE = 'i'
    FORM_IMAGE_LIST = 'a'
    # this form :)
    FORM_IMAGE_TYPE = 'image_type'
    # remove does not have a form
    REMOVE = 'r'

    image_type = forms.ChoiceField(
        choices=(
            (FORM_IMAGE, 'Upload an image and link to it'),
            (FORM_IMAGE_LIST, 'Use an existing image'),
            (REMOVE, 'Remove Image'),
        ),
        label="Choose the type of image",
    )

    class Meta:
        fields = (
            'image_type',
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

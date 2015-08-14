# -*- encoding: utf-8 -*-
from django import forms
from django.conf import settings
from django.forms.widgets import RadioFieldRenderer
from django.utils.html import (
    format_html,
    format_html_join,
)

from easy_thumbnails.files import get_thumbnailer

from base.form_utils import (
    RequiredFieldForm,
    set_widget_required,
)
from block.models import (
    ContentModel,
    Document,
    HeaderFooter,
    Image,
    Link,
    Page,
    Section,
    Template,
    TemplateSection,
    Wizard,
)


def _label_from_instance(obj):
    """The label is the image."""
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


class ImageModelChoiceField(forms.ModelChoiceField):
    """The label is the image."""

    def label_from_instance(self, obj):
        return _label_from_instance(obj)


class ImageModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """The label is the image."""

    def label_from_instance(self, obj):
        return _label_from_instance(obj)


class ContentEmptyForm(forms.ModelForm):

    class Meta:
        model = ContentModel
        fields = ()


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


class HeaderFooterForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(HeaderFooterForm, self).__init__(*args, **kwargs)
        for name in ('header', 'url_facebook', 'url_linkedin', 'url_twitter'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = HeaderFooter
        fields = (
            'header',
            'url_facebook',
            'url_linkedin',
            'url_twitter',
        )


class ImageForm(forms.ModelForm):
    """Allow the user to upload an image (for the form wizard)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        title = self.fields['title']
        title.widget.attrs.update({'class': 'pure-input-2-3'})
        set_widget_required(title)

    class Meta:
        model = Image
        fields = (
            'title',
            'image',
        )
        widgets = {
            'image': forms.FileInput,
        }


class ImageListForm(forms.Form):
    """List of images (for the form wizard)."""

    images = ImageModelChoiceField(
        queryset=Image.objects.all(),
        empty_label=None,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Image
        fields = (
            'images',
        )


class ImageMultiSelectForm(forms.Form):
    """List of images (for the form wizard)."""

    images = ImageModelMultipleChoiceField(
        queryset=Image.objects.images(),
        widget=forms.CheckboxSelectMultiple,
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
    FORM_IMAGE_MULTI_SELECT = 'c'
    # this form :)
    FORM_IMAGE_TYPE = 'image_type'
    # remove does not have a form
    REMOVE = 'r'

    FORM_CHOICES = {
        FORM_IMAGE: 'Upload an image and link to it',
        FORM_IMAGE_LIST: 'Use an existing image',
        FORM_IMAGE_MULTI_SELECT: 'Select one or more images',
        REMOVE: 'Remove image from the page',
    }

    image_type = forms.ChoiceField(label="Choose the type of image")

    def __init__(self, *args, **kwargs):
        link_type = kwargs.pop('link_type')
        super ().__init__(*args,**kwargs)
        # get the list of items (in the order displayed)
        if link_type == Wizard.SINGLE:
            items = [
                self.FORM_IMAGE_LIST,
                self.FORM_IMAGE,
                self.REMOVE,
            ]
        else:
            items = [
                self.FORM_IMAGE,
                self.FORM_IMAGE_LIST,
                self.FORM_IMAGE_MULTI_SELECT,
                self.REMOVE,
            ]
        # build the list of choices - adding the description
        choices = []
        for item in items:
            choices.append((item, self.FORM_CHOICES[item]))
        self.fields['image_type'].choices = choices

    class Meta:
        fields = (
            'image_type',
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

    FORM_CHOICES = {
        FORM_EXTERNAL_URL: 'Link to another site',
        FORM_PAGE_URL: 'Page on this site',
        FORM_DOCUMENT: 'Upload a document and link to it',
        FORM_DOCUMENT_LIST: 'Use an existing document',
        REMOVE: 'Remove Link',
    }

    link_type = forms.ChoiceField(label="Choose the type of link")

    def __init__(self, *args, **kwargs):
        link_type = kwargs.pop('link_type')
        super ().__init__(*args,**kwargs)
        # get the list of items (in the order displayed)
        # I don't think we are handling multi-links yet.
        if link_type == Wizard.SINGLE:
            items = [
                self.FORM_EXTERNAL_URL,
                self.FORM_PAGE_URL,
                self.FORM_DOCUMENT,
                self.FORM_DOCUMENT_LIST,
                self.REMOVE,
            ]
        else:
            items = [
                self.FORM_EXTERNAL_URL,
                self.FORM_PAGE_URL,
                self.FORM_DOCUMENT,
                self.FORM_DOCUMENT_LIST,
                self.REMOVE,
            ]
        # build the list of choices - adding the description
        choices = []
        for item in items:
            choices.append((item, self.FORM_CHOICES[item]))
        self.fields['link_type'].choices = choices

    class Meta:
        fields = (
            'link_type',
        )


class PageEmptyForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ()


class PageForm(RequiredFieldForm):

    template = forms.ModelChoiceField(queryset=Template.objects.all())

    class Meta:
        model = Page
        fields = (
            'name',
            'slug',
            'slug_menu',
            'order',
            'is_home',
            'template',
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


class SectionForm(RequiredFieldForm):

    class Meta:
        model = Section
        fields = (
            'name',
            'slug',
            'block_app',
            'block_model',
            'create_url_name',
            'paginated',
        )


class TemplateForm(RequiredFieldForm):

    class Meta:
        model = Template
        fields = (
            'template_name',
        )


class TemplateSectionEmptyForm(forms.ModelForm):

    class Meta:
        model = TemplateSection
        fields = ()


class TemplateSectionForm(RequiredFieldForm):

    class Meta:
        model = TemplateSection
        fields = (
            'section',
        )

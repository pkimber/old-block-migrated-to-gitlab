# -*- encoding: utf-8 -*-
from django import forms
from django.utils.html import format_html
from easy_thumbnails.files import get_thumbnailer

from base.form_utils import (
    FileDropInput,
    RequiredFieldForm,
    set_widget_required,
)
from block.models import (
    ContentModel,
    Document,
    HeaderFooter,
    Image,
    ImageCategory,
    Link,
    LinkCategory,
    MenuItem,
    Page,
    Section,
    Template,
    TemplateSection,
)


def _label_from_instance(obj):
    """The label is the image."""
    thumbnailer = get_thumbnailer(obj.image)
    thumbnail_options = {
        'crop': True,
        'size': (100, 100),
    }
    thumbnail = thumbnailer.get_thumbnail(thumbnail_options)
    return format_html('{}<br><img src="{}" />'.format(
        obj.title,
        thumbnail.url,
    ))


def _label_from_many_to_many_instance(obj):
    """The label is the image."""
    thumbnailer = get_thumbnailer(obj.image.image)
    thumbnail_options = {
        'crop': True,
        'size': (100, 100),
    }
    thumbnail = thumbnailer.get_thumbnail(thumbnail_options)
    return format_html('{}. {}<br><img src="{}" />'.format(
        obj.order,
        obj.image.title,
        thumbnail.url,
    ))


def _link_label_from_instance(obj):
    return format_html('{} (<small>{}</small>)'.format(
        obj.title,
        obj.link_type_description,
    ))


def _link_label_from_many_to_many_instance(obj):
    return format_html('{} (<small>{}</small>)'.format(
        obj.link.title,
        obj.link.link_type_description,
    ))


class ImageModelChoiceField(forms.ModelChoiceField):
    """The label is the image."""

    def label_from_instance(self, obj):
        return _label_from_instance(obj)


class ImageModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """The label is the image."""

    def label_from_instance(self, obj):
        return _label_from_instance(obj)


class LinkModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return _link_label_from_instance(obj)


class LinkModelMultipleChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return _link_label_from_instance(obj)


class LinkManyToManyMultipleChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return _link_label_from_many_to_many_instance(obj)


class ManyToManyMultipleChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return _label_from_many_to_many_instance(obj)


class ContentEmptyForm(forms.ModelForm):

    class Meta:
        model = ContentModel
        fields = ()


class DocumentForm(forms.ModelForm):
    """Allow the user to upload a document (for the form wizard)."""

    add_to_library = forms.BooleanField(
        help_text='tick this box to add the document to the library',
        initial=True,
        required=False,
    )
    category = forms.ModelChoiceField(
        queryset=LinkCategory.objects.categories(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        in_library = kwargs.pop('in_library', None)
        super().__init__(*args, **kwargs)
        for field_name in ['document', 'title']:
            field = self.fields[field_name]
            field.widget.attrs.update({'class': 'pure-input-2-3'})
            if field_name == 'title' or not in_library:
                set_widget_required(field)
        category = self.fields['category']
        category.widget.attrs.update({'class': 'pure-input-2-3'})
        if in_library:
            del self.fields['add_to_library']

    class Meta:
        model = Document
        fields = (
            'document',
            'title',
            'category',
            'add_to_library',
        )
        widgets = {
            'document': FileDropInput,
        }


class EmptyContentForm(forms.ModelForm):

    class Meta:
        model = ContentModel
        fields = ()


class EmptyForm(forms.Form):

    class Meta:
        fields = ()


class ExternalLinkForm(forms.ModelForm):
    """Enter a URL for a web site (for the form wizard)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('title', 'url_external'):
            self.fields[name].widget.attrs.update({'class': 'pure-input-2-3'})

    class Meta:
        model = Link
        fields = (
            'title',
            'url_external',
            'category',
        )


class HeaderFooterForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_names = (
            'header',
            'footer_left',
            'footer_right',
            'url_facebook',
            'url_linkedin',
            'url_twitter',
        )
        for name in field_names:
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = HeaderFooter
        fields = (
            'header',
            'footer_left',
            'footer_right',
            'url_facebook',
            'url_linkedin',
            'url_twitter',
        )


class ImageCategoryEmptyForm(forms.ModelForm):

    class Meta:
        model = ImageCategory
        fields = ()


class ImageCategoryForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'pure-input-2-3'})

    class Meta:
        model = ImageCategory
        fields = (
            'name',
        )


class ImageForm(forms.ModelForm):
    """Allow the user to upload an image (for the form wizard)."""

    add_to_library = forms.BooleanField(
        help_text='tick this box to add the image to the library',
        initial=True,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['image', 'title']:
            field = self.fields[field_name]
            field.widget.attrs.update({'class': 'pure-input-2-3'})
            set_widget_required(field)
        category = self.fields['category']
        category.queryset = ImageCategory.objects.categories()
        category.widget.attrs.update({'class': 'pure-input-2-3'})

    class Meta:
        model = Image
        fields = (
            'image',
            'title',
            'category',
            'add_to_library',
        )
        widgets = {
            'image': FileDropInput(),
        }


class ImageListDeleteForm(forms.Form):
    """List of images (so the user can delete them)."""

    images = ImageModelMultipleChoiceField(
        queryset=Image.objects.images(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        fields = (
            'images',
        )


class ImageListForm(forms.Form):
    """List of images (for the form wizard)."""

    images = ImageModelChoiceField(
        queryset=Image.objects.images(),
        empty_label=None,
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        category_slug = kwargs.pop('category_slug')
        super().__init__(*args, **kwargs)
        if category_slug:
            images = self.fields['images']
            images.queryset = Image.objects.images().filter(
                category__slug=category_slug
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
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        category_slug = kwargs.pop('category_slug')
        super().__init__(*args, **kwargs)
        if category_slug:
            images = self.fields['images']
            images.queryset = Image.objects.images().filter(
                category__slug=category_slug
            )

    class Meta:
        fields = (
            'images',
        )


class ImageSelectForm(forms.Form):
    """List of current images in the slideshow."""

    # Note: The ``queryset`` will not contain ``Image`` records.
    many_to_many = ManyToManyMultipleChoiceField(
        queryset=Image.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        qs_many_to_many = kwargs.pop('many_to_many')
        super().__init__(*args, **kwargs)
        many_to_many = self.fields['many_to_many']
        many_to_many.queryset = qs_many_to_many.order_by('order')
        # tick every link - so the user can untick the ones they want to remove
        initial = {item.pk: True for item in qs_many_to_many}
        many_to_many.initial = initial


class ImageUpdateForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        title = self.fields['title']
        title.widget.attrs.update({'class': 'pure-input-2-3'})
        set_widget_required(title)
        category = self.fields['category']
        category.queryset = ImageCategory.objects.categories()
        category.widget.attrs.update({'class': 'pure-input-2-3'})

    class Meta:
        model = Image
        fields = (
            'title',
            'category',
        )


class LinkCategoryEmptyForm(forms.ModelForm):

    class Meta:
        model = LinkCategory
        fields = ()


class LinkCategoryForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'pure-input-2-3'})

    class Meta:
        model = LinkCategory
        fields = (
            'name',
        )


class LinkEmptyForm(forms.ModelForm):

    class Meta:
        model = Link
        fields = ()


class LinkListForm(forms.Form):
    """List of links (for the form wizard)."""

    links = LinkModelChoiceField(
        queryset=Link.objects.links(),
        empty_label=None,
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        category_slug = kwargs.pop('category_slug')
        super().__init__(*args, **kwargs)
        if category_slug:
            links = self.fields['links']
            links.queryset = Link.objects.links().filter(
                category__slug=category_slug
            )

    class Meta:
        model = Link
        fields = (
            'links',
        )


class LinkMultiSelectForm(forms.Form):
    """List of links (for the form wizard)."""

    links = LinkModelMultipleChoiceField(
        queryset=Link.objects.links(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        category_slug = kwargs.pop('category_slug')
        super().__init__(*args, **kwargs)
        if category_slug:
            links = self.fields['links']
            links.queryset = Link.objects.links().filter(
                category__slug=category_slug
            )

    class Meta:
        fields = (
            'links',
        )


class LinkSelectForm(forms.Form):
    """List of current images in the slideshow."""

    # Note: The ``queryset`` will not contain ``Link`` records.
    many_to_many = LinkManyToManyMultipleChoiceField(
        queryset=Link.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        qs_many_to_many = kwargs.pop('many_to_many')
        super().__init__(*args, **kwargs)
        many_to_many = self.fields['many_to_many']
        many_to_many.queryset = qs_many_to_many.order_by('order')
        # tick every link - so the user can untick the ones they want to remove
        initial = {item.pk: True for item in qs_many_to_many}
        many_to_many.initial = initial


class MenuItemEmptyForm(forms.ModelForm):

    class Meta:
        model = MenuItem
        fields = ()


class MenuItemBaseForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('order', 'title'):
            field = self.fields[name]
            field.widget.attrs.update({'class': 'pure-input-1', 'rows': 2})
        # parent = self.fields['parent']
        # parent.queryset = MenuItem.objects.primary_items()


class MenuItemForm(MenuItemBaseForm):

    class Meta:
        model = MenuItem
        fields = (
            'order',
            'title',
        )


class PageEmptyForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ()


class PageBaseForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('meta_description', 'meta_keywords'):
            field = self.fields[name]
            field.widget.attrs.update({'class': 'pure-input-1', 'rows': 2})
        template = self.fields['template']
        template.queryset = Template.objects.templates()


class PageForm(PageBaseForm):

    class Meta:
        model = Page
        fields = (
            'name',
            'slug',
            'slug_menu',
            'order',
            'meta_description',
            'meta_keywords',
            'is_home',
            'template',
        )


class PageFormSimple(PageBaseForm):

    class Meta:
        model = Page
        fields = (
            'name',
            'template',
            'meta_description',
            'meta_keywords',
        )


class PageFormSimpleUpdate(PageBaseForm):

    class Meta:
        model = Page
        fields = (
            'name',
            'template',
            'order',
            'meta_description',
            'meta_keywords',
        )


class PageListForm(forms.ModelForm):
    """Select a page from this web site (for the form wizard)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'pure-input-2-3'})
        self.fields['url_internal'].label = 'URL'

    class Meta:
        model = Link
        fields = (
            'title',
            'url_internal',
            'category',
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
            'name',
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

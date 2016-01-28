# -*- encoding: utf-8 -*-
import pytest

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from block.models import Wizard
from block.tests.factories import ImageCategoryFactory
from example_block.tests.factories import TitleFactory
from login.tests.fixture import perm_check


def _reverse_wizard_url(content, url_name, field_name, wizard_type, category):
    """Get the wizard url for a piece of content."""
    content_type = ContentType.objects.get_for_model(content)
    kwargs = {
        'content': content_type.pk,
        'pk': content.pk,
        'field': field_name,
        'type': wizard_type,
    }
    if category:
        kwargs.update(category=category.slug)
    return reverse(url_name, kwargs=kwargs)


def url_image_multi(content, url_name, category=None):
    return _reverse_wizard_url(
        content, url_name, 'slideshow', Wizard.MULTI, category
    )


def url_image_single(content, url_name, category=None):
    return _reverse_wizard_url(
        content, url_name, 'picture', Wizard.SINGLE, category
    )


def url_link_multi(content, url_name, category=None):
    return _reverse_wizard_url(
        content, url_name, 'references', Wizard.MULTI, category
    )

def url_link_single(content, url_name, category=None):
    return _reverse_wizard_url(
        content, url_name, 'link', Wizard.SINGLE, category
    )


@pytest.mark.django_db
def test_wizard_image_choose(perm_check):
    content = TitleFactory()
    url = url_image_single(content, 'block.wizard.image.choose')
    perm_check.staff(url)


@pytest.mark.django_db
def test_wizard_image_choose_category(perm_check):
    category = ImageCategoryFactory()
    content = TitleFactory()
    url = url_image_single(content, 'block.wizard.image.choose', category=category)
    perm_check.staff(url)


@pytest.mark.django_db
def test_wizard_image_option(perm_check):
    content = TitleFactory()
    url = url_image_single(content, 'block.wizard.image.option')
    perm_check.staff(url)


@pytest.mark.django_db
def test_wizard_image_order(perm_check):
    content = TitleFactory()
    url = url_image_multi(content, 'block.wizard.image.order')
    perm_check.staff(url)


@pytest.mark.django_db
def test_wizard_image_select(perm_check):
    content = TitleFactory()
    url = url_image_single(content, 'block.wizard.image.order')
    perm_check.staff(url)


@pytest.mark.django_db
def test_wizard_image_remove(perm_check):
    content = TitleFactory()
    url = url_image_single(content, 'block.wizard.image.remove')
    perm_check.staff(url)


@pytest.mark.django_db
def test_wizard_image_select(perm_check):
    content = TitleFactory()
    url = url_image_multi(content, 'block.wizard.image.select')
    perm_check.staff(url)


@pytest.mark.django_db
def test_wizard_image_upload(perm_check):
    content = TitleFactory()
    url = url_image_single(content, 'block.wizard.image.upload')
    perm_check.staff(url)


@pytest.mark.django_db
def test_wizard_link_choose(perm_check):
    content = TitleFactory()
    url = url_link_single(content, 'block.wizard.link.choose')
    perm_check.staff(url)


@pytest.mark.django_db
def test_wizard_link_option(perm_check):
    content = TitleFactory()
    url = url_link_single(content, 'block.wizard.link.option')
    perm_check.staff(url)


@pytest.mark.django_db
def test_wizard_link_page(perm_check):
    content = TitleFactory()
    url = url_link_single(content, 'block.wizard.link.page')
    perm_check.staff(url)


@pytest.mark.django_db
def test_wizard_link_upload(perm_check):
    content = TitleFactory()
    url = url_link_single(content, 'block.wizard.link.upload')
    perm_check.staff(url)


@pytest.mark.django_db
def test_wizard_urls(perm_check):
    urls = TitleFactory().wizard_urls
    url = next(x['url'] for x in urls if 'Link' in x['caption'])
    perm_check.staff(url)

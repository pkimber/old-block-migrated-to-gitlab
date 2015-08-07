# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import NoReverseMatch
from django.db.utils import IntegrityError

from block.tests.factories import PageFactory
from block.models import (
    BlockError,
    Page,
    Url,
)


@pytest.mark.django_db
def test_create_page_url():
    page = PageFactory(slug='info', slug_menu='')
    url = Url.objects.create_page_url(page)
    assert url.name == 'project.page'
    assert url.url == '/info/'


@pytest.mark.django_db
def test_create_page_url_home():
    page = PageFactory(slug=Page.HOME, slug_menu='', is_home=True)
    url = Url.objects.create_page_url(page)
    assert url.name == 'project.home'
    assert url.url == '/'


@pytest.mark.django_db
def test_create_page_url_custom():
    page = PageFactory(slug=Page.CUSTOM, slug_menu='calendar')
    with pytest.raises(BlockError) as e:
        Url.objects.create_page_url(page)
    assert "Cannot create a URL for a custom" in str(e.value)


@pytest.mark.django_db
def test_create_page_url_deleted():
    page = PageFactory(slug='info', slug_menu='', deleted=True)
    with pytest.raises(BlockError) as e:
        Url.objects.create_page_url(page)
    assert "Cannot create a URL for a deleted" in str(e.value)


@pytest.mark.django_db
def test_create_page_url_is_custom():
    page = PageFactory(slug='event', slug_menu='calendar', is_custom=True)
    with pytest.raises(BlockError) as e:
        Url.objects.create_page_url(page)
    assert "Cannot create a URL for a custom" in str(e.value)


@pytest.mark.django_db
def test_create_reverse_url():
    url = Url.objects.create_reverse_url('project.settings')
    assert '/settings/' == url.url


@pytest.mark.django_db
def test_create_reverse_url_duplicate():
    Url.objects.create_reverse_url('project.settings')
    with pytest.raises(IntegrityError) as e:
        Url.objects.create_reverse_url('project.settings')
    assert "UNIQUE constraint failed: block_url.name," in str(e.value)


@pytest.mark.django_db
def test_create_reverse_url_invalid():
    with pytest.raises(NoReverseMatch) as e:
        Url.objects.create_reverse_url('project.settings', 'does-not-exist')
    assert "Reverse for 'project.settings' with arguments" in str(e.value)


@pytest.mark.django_db
def test_create_reverse_url_slug():
    url = Url.objects.create_reverse_url('project.page.design', 'info')
    assert '/info/design/' == url.url


@pytest.mark.django_db
def test_create_reverse_url_slug_menu():
    url = Url.objects.create_reverse_url('project.page.design', 'info', 'data')
    assert '/info/data/design/' == url.url

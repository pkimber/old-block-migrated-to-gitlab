# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import NoReverseMatch

from block.tests.factories import PageFactory
from block.models import (
    BlockError,
    Page,
    Url,
)


@pytest.mark.django_db
def test_init_page_url():
    page = PageFactory(name='Information', slug='info', slug_menu='')
    url = Url.objects.init_page_url(page)
    assert url.title == 'Information'
    assert url.url == '/info/'


@pytest.mark.django_db
def test_init_page_url_home():
    page = PageFactory(name='Home', slug=Page.HOME, slug_menu='', is_home=True)
    url = Url.objects.init_page_url(page)
    assert url.title == 'Home'
    assert url.url == '/'


@pytest.mark.django_db
def test_init_page_url_custom():
    page = PageFactory(slug=Page.CUSTOM, slug_menu='calendar')
    with pytest.raises(BlockError) as e:
        Url.objects.init_page_url(page)
    assert "Cannot create a URL for a custom" in str(e.value)


@pytest.mark.django_db
def test_init_page_url_deleted():
    page = PageFactory(slug='info', slug_menu='', deleted=True)
    with pytest.raises(BlockError) as e:
        Url.objects.init_page_url(page)
    assert "Cannot create a URL for a deleted" in str(e.value)


@pytest.mark.django_db
def test_init_page_url_duplicate_change_name():
    page = PageFactory(name='Info 1', slug='info', slug_menu='')
    Url.objects.init_page_url(page)
    page.name = 'Info 2'
    page.save()
    url = Url.objects.init_page_url(page)
    assert 'Info 2' == url.title


@pytest.mark.django_db
def test_init_page_url_is_custom():
    page = PageFactory(slug='event', slug_menu='calendar', is_custom=True)
    with pytest.raises(BlockError) as e:
        Url.objects.init_page_url(page)
    assert "Cannot create a URL for a custom" in str(e.value)


@pytest.mark.django_db
def test_init_reverse_url():
    url = Url.objects.init_reverse_url('Settings', 'project.settings')
    assert '/settings/' == url.url


@pytest.mark.django_db
def test_init_reverse_url_duplicate_change__title():
    Url.objects.init_reverse_url('Settings 1', 'project.settings')
    url = Url.objects.init_reverse_url('Settings 2', 'project.settings')
    assert 'Settings 2' == url.title


@pytest.mark.django_db
def test_init_reverse_url_invalid():
    with pytest.raises(NoReverseMatch) as e:
        Url.objects.init_reverse_url(
            'A page which does not exist', 'project.settings', 'does-not-exist'
        )
    assert "Reverse for 'project.settings' with arguments" in str(e.value)


@pytest.mark.django_db
def test_init_reverse_url_is_custom():
    PageFactory(slug=Page.CUSTOM, slug_menu='calendar', is_custom=True)
    url = Url.objects.init_reverse_url(
        'Calendar',
        'calendar.information',
    )
    assert '/calendar/information/' == url.url


@pytest.mark.django_db
def test_init_reverse_url_slug():
    url = Url.objects.init_reverse_url(
        'Design', 'project.page.design', 'info'
    )
    assert '/info/design/' == url.url


@pytest.mark.django_db
def test_init_reverse_url_slug_menu():
    url = Url.objects.init_reverse_url(
        'Design', 'project.page.design', 'info', 'data'
    )
    assert '/info/data/design/' == url.url


@pytest.mark.django_db
def test_init_pages():
    PageFactory(name='a', slug='info', slug_menu='')
    PageFactory(name='b', slug='info', slug_menu='data')
    PageFactory(name='c', slug='info', slug_menu='open', is_custom=True)
    Url.objects.init_pages()
    result = [item.title for item in Url.objects.urls()]
    assert ['a', 'b'] == result


@pytest.mark.django_db
def test_init_pages_repeat():
    PageFactory(name='a', slug='info', slug_menu='')
    PageFactory(name='b', slug='info', slug_menu='data')
    Url.objects.init_pages()
    Url.objects.init_pages()
    result = [item.title for item in Url.objects.urls()]
    assert ['a', 'b'] == result

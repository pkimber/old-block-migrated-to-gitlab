# -*- encoding: utf-8 -*-
import pytest

from block.tests.factories import (
    PageFactory,
    UrlFactory,
)


@pytest.mark.django_db
def test_url():
    url = UrlFactory(name='block.page.list')
    assert '/block/page/list/' == url.url


@pytest.mark.django_db
def test_url_custom():
    url = UrlFactory(name='calendar.information')
    assert '/calendar/information/' == url.url


@pytest.mark.django_db
def test_url_page():
    PageFactory(slug='home')
    url = UrlFactory(name='project.page', arg1='home')
    assert '/home/' == url.url


@pytest.mark.django_db
def test_url_page_menu():
    PageFactory(slug='sport', slug_menu='football')
    url = UrlFactory(name='project.page', arg1='sport', arg2='football')
    assert '/sport/football/' == url.url

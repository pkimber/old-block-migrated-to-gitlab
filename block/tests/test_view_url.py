# -*- encoding: utf-8 -*-
import pytest

from block.models import ViewUrl
from block.tests.factories import PageFactory
from login.tests.factories import UserFactory


@pytest.mark.django_db
def test_str_custom():
    url = ViewUrl.objects.view_url(
        UserFactory(),
        PageFactory(is_custom=True),
        '/contact/23/'
    )
    assert '/contact/23/' == url


@pytest.mark.django_db
def test_str_not_custom():
    url = ViewUrl.objects.view_url(
        UserFactory(),
        PageFactory(slug='contact', slug_menu='office'),
        None
    )
    assert '/contact/office/' == url


@pytest.mark.django_db
def test_custom_empty_get_previous():
    user = UserFactory()
    page = PageFactory(is_custom=True)
    ViewUrl.objects.view_url(user, page, '/contact/23/')
    url = ViewUrl.objects.view_url(user, page, None)
    assert '/contact/23/' == url


@pytest.mark.django_db
def test_custom_empty_get_empty():
    url = ViewUrl.objects.view_url(
        UserFactory(),
        PageFactory(is_custom=True),
        None,
    )
    assert '' == url

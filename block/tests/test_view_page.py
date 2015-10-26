# -*- encoding: utf-8 -*-
import pytest
from django.core.urlresolvers import reverse
from django.test import TestCase

from block.models import Page
from login.tests.factories import (
    TEST_PASSWORD,
    UserFactory,
)


@pytest.mark.django_db
def test_home(client):
    page = Page.objects.init_page(
        Page.HOME, '', 'Home', 0, 'example/page.html', is_home=True
    )
    response = client.get(reverse('project.home'))
    assert 200 == response.status_code


@pytest.mark.django_db
def test_custom(client):
    page = Page.objects.init_page(
        Page.CUSTOM, 'contact', 'Contact', 1, 'example/page.html'
    )
    url = reverse('project.page', args=[Page.CUSTOM, 'contact'])
    response = client.get(url)
    assert 200 == response.status_code


@pytest.mark.django_db
def test_custom_does_not_exist(client):
    url = reverse('project.page', args=[Page.CUSTOM, 'does-not-exist'])
    response = client.get(url)
    assert 404 == response.status_code

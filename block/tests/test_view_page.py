# -*- encoding: utf-8 -*-
import pytest
from django.core.urlresolvers import reverse
from django.test import TestCase

from block.models import Page, Url
from block.tests.factories import PageFactory, TemplateFactory
from login.tests.factories import TEST_PASSWORD, UserFactory


@pytest.mark.django_db
def test_home(client):
    page = Page.objects.init_page(
        Page.HOME,
        '',
        'Home',
        0,
        TemplateFactory(template_name='example/page.html'),
        is_home=True
    )
    response = client.get(reverse('project.home'))
    assert 200 == response.status_code


@pytest.mark.django_db
def test_custom(client):
    page = Page.objects.init_page(
        Page.CUSTOM,
        'contact',
        'Contact',
        1,
        TemplateFactory(template_name='example/page.html'),
    )
    url = reverse('project.page', args=[Page.CUSTOM, 'contact'])
    response = client.get(url)
    assert 200 == response.status_code


@pytest.mark.django_db
def test_custom_does_not_exist(client):
    url = reverse('project.page', args=[Page.CUSTOM, 'does-not-exist'])
    response = client.get(url)
    assert 404 == response.status_code


@pytest.mark.django_db
def test_page_create(client):
    """Create a page and make sure the list of URLs is updated."""
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    template = TemplateFactory()
    data = {
        'name': 'Apple',
        'template': template.pk,
    }
    response = client.post(reverse('block.page.create'), data)
    assert 302 == response.status_code, response.context['form'].errors
    assert reverse('block.page.list') == response['location']
    assert 1 == Page.objects.count()
    page = Page.objects.first()
    url = Url.objects.get(page=page)
    assert page.name == url.title


@pytest.mark.django_db
def test_page_update(client):
    """Update a page and make sure the list of URLs is updated."""
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    template = TemplateFactory()
    page = PageFactory(name='Orange', template=template)
    data = {
        'name': 'Apple',
        'order': 3,
        'template': template.pk,
    }
    response = client.post(reverse('block.page.update', args=[page.pk]), data)
    assert 302 == response.status_code, response.context['form'].errors
    assert reverse('block.page.list') == response['location']
    page.refresh_from_db()
    url = Url.objects.get(page=page)
    assert page.name == url.title

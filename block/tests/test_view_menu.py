# -*- encoding: utf-8 -*-
import pytest
from django.core.urlresolvers import reverse
# from django.test import TestCase

from block.models import Menu, MenuItem
from block.tests.factories import (
    MenuFactory,
    MenuItemFactory,
)
from login.tests.factories import TEST_PASSWORD, UserFactory


# @pytest.mark.django_db
# def test_home(client):
#     page = Page.objects.init_page(
#         Page.HOME,
#         '',
#         'Home',
#         0,
#         TemplateFactory(template_name='example/page.html'),
#         is_home=True
#     )
#     response = client.get(reverse('project.home'))
#     assert 200 == response.status_code


# @pytest.mark.django_db
# def test_custom(client):
#     page = Page.objects.init_page(
#         Page.CUSTOM,
#         'contact',
#         'Contact',
#         1,
#         TemplateFactory(template_name='example/page.html'),
#     )
#     url = reverse('project.page', args=[Page.CUSTOM, 'contact'])
#     response = client.get(url)
#     assert 200 == response.status_code


# @pytest.mark.django_db
# def test_custom_does_not_exist(client):
#     url = reverse('project.page', args=[Page.CUSTOM, 'does-not-exist'])
#     response = client.get(url)
#     assert 404 == response.status_code


@pytest.mark.django_db
def test_navigation_menu_creates_menu_on_first_run(client):
    """Navigation Menu View should create menu if does not exist.
    Subsequent runs should use the existing menu
    """
    user = UserFactory(is_staff=True)
    assert Menu.objects.navigation_menu_items() is None
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = reverse('block.menuitem.list', args=[Menu.NAVIGATION])
    response = client.get(url)

    assert response.status_code == 200
    menu = Menu.objects.get(slug=Menu.NAVIGATION)
    assert menu.title == "Navigation Menu"
    # run second time
    response = client.get(url)
    #  no menu created
    assert Menu.objects.count() == 1


@pytest.mark.django_db
def test_menuitem_create(client):
    """Create a menuitem and check it's in the navigation menu."""
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    menu = MenuFactory(slug=Menu.NAVIGATION)
    data = {
        'title': 'Home',
        'order': '1',
    }
    response = client.post(
        reverse('block.menuitem.create', args=[menu.slug]), data
    )
    assert 302 == response.status_code, response.context['form'].errors
    expect = reverse('block.menuitem.list', args=[menu.slug])
    assert expect == response['location']
    assert 1 == MenuItem.objects.count()
    assert ['home'] == [m.slug for m in Menu.objects.navigation_menu_items()]


@pytest.mark.django_db
def test_menuitem_update(client):
    """Update a menuitem and check it's in the navigation menu."""
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    menu = MenuFactory(slug=Menu.NAVIGATION)
    menu_item = MenuItemFactory(menu=menu)
    data = {
        'title': 'Home',
        'order': '4',
    }
    response = client.post(
        reverse('block.menuitem.update', args=[menu_item.pk]), data
    )
    assert 302 == response.status_code, response.context['form'].errors
    expect = reverse('block.menuitem.list', args=[menu.slug])
    assert expect == response['location']
    assert 1 == MenuItem.objects.count()
    assert [('Home', 4)] == [
        (m.title, m.order) for m in Menu.objects.navigation_menu_items()
    ]


@pytest.mark.django_db
def test_menuitem_delete(client):
    """Delete a menuitem and check it's not in the navigation menu."""
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    menu = MenuFactory(slug=Menu.NAVIGATION)
    menu_item = MenuItemFactory(menu=menu, title="Home", slug="home")
    response = client.post(
        reverse('block.menuitem.delete', args=[menu_item.pk]), {}
    )
    assert 302 == response.status_code, response.context['form'].errors
    expect = reverse('block.menuitem.list', args=[menu.slug])
    assert expect == response['location']
    assert 1 == MenuItem.objects.count()
    menu_item.refresh_from_db()
    assert menu_item.is_deleted
    assert [] == [m.title for m in Menu.objects.navigation_menu_items()]

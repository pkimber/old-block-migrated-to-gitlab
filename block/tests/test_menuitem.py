# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

from block.models import (
    Link,
    Menu,
    # MenuItem,
    Url,
)
from block.tests.factories import (
    # LinkFactory,
    MenuFactory,
    MenuItemFactory,
    PageFactory,
)


@pytest.mark.django_db
def test_get_design_url():
    menu = MenuFactory(slug='main', title='Main Menu')
    menu_item = MenuItemFactory(menu=menu, slug='main-1', title='One')

    menu_list_url = reverse('block.menuitem.list', args=[menu.slug])
    assert menu_item.get_design_url() == menu_list_url


@pytest.mark.django_db
def test_navigation_menu():
    menu = MenuFactory(slug='main')
    MenuItemFactory(menu=menu, slug='past', deleted=True)
    MenuItemFactory(menu=menu, slug='present')
    MenuItemFactory(menu=menu, slug='future')
    assert 2 == len(Menu.objects.navigation_menu_items())
    assert ['present', 'future'] == [
        m.slug for m in Menu.objects.navigation_menu_items()
    ]


@pytest.mark.django_db
def test_menu_link_none():
    menu = MenuFactory(slug='main')
    menu_item = MenuItemFactory(menu=menu, slug='present')
    assert 1 == len(Menu.objects.navigation_menu_items())
    assert menu_item.get_link() == '#'


@pytest.mark.django_db
def test_menu_link_external():
    menu = MenuFactory(slug='main')
    menu_item = MenuItemFactory(menu=menu, slug='present')
    menu_item.link = Link.objects.create_external_link(
        'http://www.bbc.co.uk/', 'News'
    )
    menu_item.save()
    assert menu_item.get_link() == 'http://www.bbc.co.uk/'


@pytest.mark.django_db
def test_menu_link_internal():
    menu = MenuFactory(slug='main')
    page = PageFactory(slug='current', slug_menu='day')
    menu_item = MenuItemFactory(menu=menu, slug='present')
    menu_item.link = Link.objects.create_internal_link(
        Url.objects.init_page_url(page)
    )
    menu_item.save()
    menu_item.refresh_from_db()
    assert menu_item.get_link() == '/current/day/'

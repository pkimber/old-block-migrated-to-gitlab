# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

from block.models import (
    Link,
    Menu,
    MenuItem,
    Url,
)
from block.tests.factories import (
    MenuFactory,
    MenuItemFactory,
    PageFactory,
)


@pytest.mark.django_db
def test_get_design_url():
    menu = MenuFactory(slug=Menu.NAVIGATION, title='Main Menu')
    menu_item = MenuItemFactory(menu=menu, slug='main-1', title='One')

    menu_list_url = reverse('block.menuitem.list', args=[menu.slug])
    assert menu_item.get_design_url() == menu_list_url


@pytest.mark.django_db
def test_navigation_menu():
    menu = MenuFactory(slug=Menu.NAVIGATION)
    MenuItemFactory(menu=menu, slug='past', deleted=True)
    MenuItemFactory(menu=menu, slug='present')
    MenuItemFactory(menu=menu, slug='future')
    assert 2 == len(Menu.objects.navigation_menu_items())
    assert ['present', 'future'] == [
        m.slug for m in Menu.objects.navigation_menu_items()
    ]


@pytest.mark.django_db
def test_menu_link_none():
    menu = MenuFactory(slug=Menu.NAVIGATION)
    menu_item = MenuItemFactory(menu=menu, slug='present')
    assert 1 == len(Menu.objects.navigation_menu_items())
    assert menu_item.get_link() == '#'


@pytest.mark.django_db
def test_menu_link_external():
    menu = MenuFactory(slug=Menu.NAVIGATION)
    menu_item = MenuItemFactory(menu=menu, slug='present')
    menu_item.link = Link.objects.create_external_link(
        'http://www.bbc.co.uk/', 'News'
    )
    menu_item.save()
    assert menu_item.get_link() == 'http://www.bbc.co.uk/'


@pytest.mark.django_db
def test_menu_link_internal():
    menu = MenuFactory(slug=Menu.NAVIGATION)
    page = PageFactory(slug='current', slug_menu='day')
    menu_item = MenuItemFactory(menu=menu, slug='present')
    menu_item.link = Link.objects.create_internal_link(
        Url.objects.init_page_url(page)
    )
    menu_item.save()
    menu_item.refresh_from_db()
    assert menu_item.get_link() == '/current/day/'


@pytest.mark.django_db
def test_create_menuitem():
    menu = MenuFactory(slug=Menu.NAVIGATION)
    MenuItem.objects.create_menuitem(
        menu=menu, slug='main-2', title='Two', order=2,
        link=Link.objects.create_external_link('http://www.bbc.co.uk/', 'BBC')
    )
    MenuItem.objects.create_menuitem(
        menu=menu, slug='main-1', title='One', order=1,
        link=Link.objects.create_external_link(
            'http://news.bbc.co.uk/', 'News'
        )
    )

    menuitems = Menu.objects.navigation_menu_items()
    assert ['One', 'Two'] == [item.title for item in menuitems]
    assert ['http://news.bbc.co.uk/', 'http://www.bbc.co.uk/'] == [
        item.get_link() for item in menuitems
    ]


@pytest.mark.django_db
def test_init_menuitem_create():
    menu = MenuFactory(slug=Menu.NAVIGATION)
    link = Link.objects.create_external_link('http://www.bbc.co.uk/', 'BBC')
    item = MenuItem.objects.init_menuitem(
        menu=menu, slug='main-1', title='test', order=1, link=link
    )
    assert item.title == 'test'
    assert item.order == 1
    assert item.get_link() == 'http://www.bbc.co.uk/'


@pytest.mark.django_db
def test_init_menuitem_update():
    menu = MenuFactory(slug=Menu.NAVIGATION)
    item = MenuItemFactory(menu=menu, slug='main-1', title='x', order=0)
    assert item.menu == menu
    assert item.slug == 'main-1'
    assert item.title == 'x'
    assert item.order == 0
    assert item.get_link() == '#'
    link = Link.objects.create_external_link('http://www.bbc.co.uk/', 'BBC')
    item = MenuItem.objects.init_menuitem(
        menu=menu, slug='main-1', title='test', order=1, link=link
    )
    assert item.menu == menu
    assert item.slug == 'main-1'
    assert item.title == 'test'
    assert item.order == 1
    assert item.get_link() == 'http://www.bbc.co.uk/'


@pytest.mark.django_db
def test_menuitem_has_children():
    menu = MenuFactory(slug=Menu.NAVIGATION)
    parent = MenuItemFactory(menu=menu, slug='main-1', title='x')
    item = MenuItemFactory(menu=menu, slug='main-2', title='x', parent=parent)

    assert parent.has_children()
    assert not item.has_children()


@pytest.mark.django_db
def test_menuitem_has_link():
    menu = MenuFactory(slug=Menu.NAVIGATION)
    item = MenuItemFactory(menu=menu, slug='main-1', title='x')

    assert not item.has_link()
    item.link = Link.objects.create_external_link('http://bbc.co.uk/', 'BBC')
    item.save()
    item.refresh_from_db()
    assert item.has_link()


@pytest.mark.django_db
def test_menuitem_get_content_object():
    menu = MenuFactory(slug=Menu.NAVIGATION)
    item = MenuItemFactory(menu=menu, slug='main-1', title='x')
    ct = item.get_content_type()
    assert ct.app_label == 'block'
    assert ct.model == 'menuitem'


@pytest.mark.django_db
def test_menuitem_set_pending_edit():
    menu = MenuFactory(slug=Menu.NAVIGATION)
    item = MenuItemFactory(menu=menu, slug='main-1', title='x')
    pe = item.set_pending_edit()
    assert pe is None

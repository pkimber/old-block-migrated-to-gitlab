# -*- encoding: utf-8 -*-
import pytest

# from django.core.urlresolvers import reverse
from django.db import IntegrityError

from block.models import (
    Menu,
)
from block.tests.factories import (
    MenuFactory,
)


@pytest.mark.django_db
def test_create_menu():
    Menu.objects.create_menu(slug=Menu.NAVIGATION, title='Navigation Menu')

    menu = Menu.objects.get(slug=Menu.NAVIGATION)
    assert menu.title == 'Navigation Menu'


@pytest.mark.django_db
def test_create_menu_already_exists():
    MenuFactory(slug=Menu.NAVIGATION)
    with pytest.raises(IntegrityError) as e:
        Menu.objects.create_menu(slug=Menu.NAVIGATION, title="Navigation Menu")
    assert e.exconly() == (
        'django.db.utils.IntegrityError: UNIQUE constraint failed:'
        ' block_menu.slug'
    )


@pytest.mark.django_db
def test_init_menu_create():
    menu = Menu.objects.init_menu(slug=Menu.NAVIGATION, title='test')
    assert menu.title == 'test'
    assert menu.navigation


@pytest.mark.django_db
def test_init_menu_update_not_navigation():
    menu = MenuFactory(slug=Menu.NAVIGATION, title="Nav menu")
    assert menu.title == "Nav menu"
    menu = Menu.objects.init_menu(
        slug=Menu.NAVIGATION, title='test', navigation=False
    )
    assert menu.title == 'test'
    assert menu.navigation is False


@pytest.mark.django_db
def test_init_menu_update_is_navigation():
    menu = MenuFactory(slug=Menu.NAVIGATION, title="Nav menu")
    assert menu.title == "Nav menu"
    menu = Menu.objects.init_menu(
        slug=Menu.NAVIGATION, title='test', navigation=True
    )
    assert menu.title == 'test'
    assert menu.navigation

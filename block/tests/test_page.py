# -*- encoding: utf-8 -*-
import pytest

from block.models import Page
from block.tests.factories import PageFactory


@pytest.mark.django_db
def test_init_not():
    try:
        Page.objects.get(slug=Page.HOME)
        pytest.fail(
            "'{}' page exists, but hasn't been "
            "created yet".format(Page.HOME)
        )
    except Page.DoesNotExist:
        pass


@pytest.mark.django_db
def test_init():
    Page.objects.init_page('Home', Page.HOME, '', 0, 'home.html')
    try:
        Page.objects.get(slug=Page.HOME)
    except Page.DoesNotExist:
        pytest.fail("'{}' page was not initialised".format(Page.HOME))


@pytest.mark.django_db
def test_init_change_order():
    # create page (order 1)
    Page.objects.init_page('Home', Page.HOME, '', 1, 'home.html')
    page = Page.objects.get(slug=Page.HOME)
    assert 1 == page.order
    # update page (order 3)
    Page.objects.init_page('Home', Page.HOME, '', 3, 'my.html')
    page = Page.objects.get(slug=Page.HOME)
    assert 3 == page.order
    assert 'my.html' == page.template_name


@pytest.mark.django_db
def test_init_is_home():
    Page.objects.init_page('Home', Page.HOME, '', 0, 'home.html', is_home=True)
    page = Page.objects.get(slug=Page.HOME)
    assert True == page.is_home


@pytest.mark.django_db
def test_init_is_not_home():
    Page.objects.init_page('Home', Page.HOME, '' , 0, 'home.html')
    page = Page.objects.get(slug=Page.HOME)
    assert False == page.is_home


@pytest.mark.django_db
def test_init_set_home():
    # create page (is not a home page)
    Page.objects.init_page('Home', Page.HOME, '', 0, 'home.html')
    page = Page.objects.get(slug=Page.HOME)
    assert False == page.is_home
    # update page (is now a home page)
    Page.objects.init_page('Home', Page.HOME, '', 0, 'home.html', is_home=True)
    page = Page.objects.get(slug=Page.HOME)
    assert True == page.is_home


@pytest.mark.django_db
def test_menu():
    PageFactory(slug='home', order=0)
    PageFactory(slug='history', deleted=True)
    PageFactory(slug='custom', custom=True)
    PageFactory(slug='info')
    PageFactory(slug='portfolio')
    assert 2 == len(Page.objects.menu())


@pytest.mark.django_db
def test_menu_in():
    PageFactory(slug='home', order=0)
    PageFactory(slug='history', deleted=True)
    PageFactory(slug='custom', custom=True)
    PageFactory(slug='info')
    PageFactory(slug='portfolio')
    result = [p.slug for p in Page.objects.menu()]
    assert ['info', 'portfolio'] == result


@pytest.mark.django_db
def test_pages():
    PageFactory(slug='home', order=0)
    PageFactory(slug='history', deleted=True)
    PageFactory(slug='custom', custom=True)
    PageFactory(slug='info')
    PageFactory(slug='portfolio')
    result = [p.slug for p in Page.objects.pages()]
    assert ['home', 'info', 'portfolio'] == result

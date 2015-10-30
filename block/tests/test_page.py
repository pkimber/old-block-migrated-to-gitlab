# -*- encoding: utf-8 -*-
import pytest

from block.models import (
    Page,
    Template,
)
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
    template = Template.objects.init_template('Home', 'home.html')
    Page.objects.init_page(Page.HOME, '', 'Home', 0, template)
    try:
        Page.objects.get(slug=Page.HOME)
    except Page.DoesNotExist:
        pytest.fail("'{}' page was not initialised".format(Page.HOME))


@pytest.mark.django_db
def test_init_change_order():
    template = Template.objects.init_template('Home', 'home.html')
    # create page (order 1)
    Page.objects.init_page(Page.HOME, '', 'Home', 1, template)
    page = Page.objects.get(slug=Page.HOME)
    assert 1 == page.order
    # update page (order 3)
    template = Template.objects.init_template('My Template', 'my.html')
    Page.objects.init_page(Page.HOME, '', 'Home', 3, template)
    page = Page.objects.get(slug=Page.HOME)
    assert 3 == page.order
    assert 'my.html' == page.template.template_name


@pytest.mark.django_db
def test_init_is_home():
    template = Template.objects.init_template('Home', 'home.html')
    Page.objects.init_page(Page.HOME, '', 'Home', 0, template, is_home=True)
    page = Page.objects.get(slug=Page.HOME)
    assert True == page.is_home


@pytest.mark.django_db
def test_init_is_not_home():
    template = Template.objects.init_template('Home', 'home.html')
    Page.objects.init_page(Page.HOME, '', 'Home' , 0, template)
    page = Page.objects.get(slug=Page.HOME)
    assert False == page.is_home


@pytest.mark.django_db
def test_init_set_home():
    template = Template.objects.init_template('Home', 'home.html')
    # create page (is not a home page)
    Page.objects.init_page(Page.HOME, '', 'Home', 0, template)
    page = Page.objects.get(slug=Page.HOME)
    assert False == page.is_home
    # update page (is now a home page)
    Page.objects.init_page(Page.HOME, '', 'Home', 0, template, is_home=True)
    page = Page.objects.get(slug=Page.HOME)
    assert True == page.is_home


@pytest.mark.django_db
def test_menu():
    PageFactory(slug='home', order=0)
    PageFactory(slug='history', deleted=True)
    PageFactory(slug=Page.CUSTOM, is_custom=True)
    PageFactory(slug='info')
    PageFactory(slug='portfolio')
    assert 2 == len(Page.objects.menu())


@pytest.mark.django_db
def test_menu_in():
    PageFactory(slug='home', order=0)
    PageFactory(slug='history', deleted=True)
    PageFactory(slug=Page.CUSTOM, is_custom=True)
    PageFactory(slug='info')
    PageFactory(slug='portfolio')
    result = [p.slug for p in Page.objects.menu()]
    assert ['info', 'portfolio'] == result


@pytest.mark.django_db
def test_page_list():
    PageFactory(slug='home', order=0)
    PageFactory(slug='history', deleted=True)
    PageFactory(slug=Page.CUSTOM, is_custom=True)
    PageFactory(slug='info')
    PageFactory(slug='portfolio')
    result = [p.slug for p in Page.objects.page_list()]
    assert ['home', 'custom', 'info', 'portfolio'] == result


@pytest.mark.django_db
def test_page_get_next_order():
    PageFactory(order=4)
    assert 5 == Page.objects.next_order()


@pytest.mark.django_db
def test_page_get_next_order_no_pages():
    assert 1 == Page.objects.next_order()


@pytest.mark.django_db
def test_pages():
    PageFactory(slug='home', order=0)
    PageFactory(slug='history', deleted=True)
    PageFactory(slug=Page.CUSTOM, is_custom=True)
    PageFactory(slug='info')
    PageFactory(slug='portfolio')
    result = [p.slug for p in Page.objects.pages()]
    assert ['home', 'info', 'portfolio'] == result

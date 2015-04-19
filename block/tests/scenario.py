# -*- encoding: utf-8 -*-
from block.models import (
    Page,
    PageSection,
    Section,
)


def get_page_custom_calendar():
    return Page.objects.get(slug=Page.CUSTOM, slug_menu='calendar-information')


def get_page_home():
    return Page.objects.get(slug=Page.HOME)


def get_page_info():
    return Page.objects.get(slug='info')


def get_page_section_home_body():
    return PageSection.objects.get(
        page=get_page_home(),
        section=get_section_body()
    )


def get_page_section_information_body():
    return PageSection.objects.get(
        page=get_page_info(),
        section=get_section_body()
    )


def get_section_body():
    return Section.objects.get(slug='body')


def default_scenario_block():
    # body section
    body = Section.objects.init_section(
        'body', 'Body', 'example_block', 'Title', 'example.title.create'
    )
    # home
    home = Page.objects.init_page(
        Page.HOME, '', 'Home', 0, 'example/page.html', is_home=True
    )
    PageSection.objects.init_page_section(home, body)
    # information
    information = Page.objects.init_page(
        'info', '', 'Information', 1, 'example/page.html'
    )
    PageSection.objects.init_page_section(information, body)
    # contact
    contact = Page.objects.init_page(
        'contact', '', 'Contact', 2, 'example/page.html'
    )
    PageSection.objects.init_page_section(contact, body)
    # custom page ('slug' == Page.CUSTOM)
    calendar = Page.objects.init_page(
        Page.CUSTOM,
        'calendar-information',
        'Calendar',
        3,
        'example/calendar-information.html',
        is_custom=True
    )
    PageSection.objects.init_page_section(calendar, body)

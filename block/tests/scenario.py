# -*- encoding: utf-8 -*-
from block.models import (
    Page,
    PageSection,
    Section,
)


def get_page_home():
    return Page.objects.get(slug=Page.HOME)


def get_page_information():
    return Page.objects.get(slug='info')


def get_page_section_home_body():
    return PageSection.objects.get(
        page=get_page_home(),
        section=get_section_body()
    )


def get_page_section_information_body():
    return PageSection.objects.get(
        page=get_page_information(),
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
    calendar = Page.objects.init_page(
        'Calendar', 'home', '', 1, 'example/calendar-information.html'
    )
    PageSection.objects.init_page_section(calendar, body)
    # home
    home = Page.objects.init_page(
        'Home', Page.HOME, '', 0, 'example/page.html', is_home=True
    )
    PageSection.objects.init_page_section(home, body)
    # information
    information = Page.objects.init_page(
        'Information', 'info', '', 1, 'example/page.html'
    )
    PageSection.objects.init_page_section(information, body)
    # contact
    contact = Page.objects.init_page(
        'Contact', 'contact', '', 2, 'example/page.html'
    )
    PageSection.objects.init_page_section(contact, body)

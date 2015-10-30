# -*- encoding: utf-8 -*-
from block.models import (
    ImageCategory,
    LinkCategory,
    Page,
    PageSection,
    Section,
    Template,
    TemplateSection,
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
    template = Template.objects.init_template('Page', 'example/page.html')
    TemplateSection.objects.init_template_section(template, body)
    home = Page.objects.init_page(
        Page.HOME, '', 'Home', 0, template, is_home=True
    )
    PageSection.objects.init_page_section(home, body)
    # information
    information = Page.objects.init_page('info', '', 'Info', 1, template)
    PageSection.objects.init_page_section(information, body)
    # contact
    contact = Page.objects.init_page('contact', '', 'Contact', 2, template)
    PageSection.objects.init_page_section(contact, body)
    # custom page ('slug' == Page.CUSTOM)
    template = Template.objects.init_template(
        'Calendar',
        'example/calendar-information.html'
    )
    TemplateSection.objects.init_template_section(template, body)
    calendar = Page.objects.init_page(
        Page.CUSTOM,
        'calendar-information',
        'Calendar',
        3,
        template,
        is_custom=True
    )
    PageSection.objects.init_page_section(calendar, body)
    ImageCategory.objects.init_category('Computers')
    ImageCategory.objects.init_category('Fruit')
    LinkCategory.objects.init_category('Contract')
    LinkCategory.objects.init_category('User Guide')

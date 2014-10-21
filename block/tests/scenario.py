# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from block.models import (
    ADD,
    EDIT,
    EditState,
    ModerateState,
    Page,
    PageSection,
    PENDING,
    PUBLISHED,
    PUSH,
    REMOVED,
    Section,
)
from block.service import (
    init_page,
    init_page_section,
    init_section,
)
from block.tests.model_maker import (
    make_edit_state,
    make_moderate_state,
)


def get_page_home():
    return Page.objects.get(slug='home')


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


def init_app_block():
    """Edit and moderate state."""
    try:
        EditState._add()
    except EditState.DoesNotExist:
        make_edit_state(ADD)
    try:
        EditState._edit()
    except EditState.DoesNotExist:
        make_edit_state(EDIT)
    try:
        EditState._push()
    except EditState.DoesNotExist:
        make_edit_state(PUSH)
    # moderate state
    try:
        ModerateState._pending()
    except ModerateState.DoesNotExist:
        make_moderate_state(PENDING)
    try:
        ModerateState._published()
    except ModerateState.DoesNotExist:
        make_moderate_state(PUBLISHED)
    try:
        ModerateState._removed()
    except ModerateState.DoesNotExist:
        make_moderate_state(REMOVED)


def default_scenario_block():
    init_app_block()
    # body section
    body = init_section(
        'Body',
        'example',
        'Title',
        'example.title.create'
    )
    # home
    home = init_page(
        'Home',
        'home',
        0,
        'example/page.html'
    )
    init_page_section(home, body)
    # information
    information = init_page(
        'Information',
        'info',
        1,
        'example/page.html'
    )
    init_page_section(information, body)
    # contact
    contact = init_page(
        'Contact',
        'contact',
        2,
        'example/page.html'
    )
    init_page_section(contact, body)

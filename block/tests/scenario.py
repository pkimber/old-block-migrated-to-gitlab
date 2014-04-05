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
    return Page.objects.get(slug='information')


def get_page_section_home_body():
    return PageSection.objects.get(
        page=get_page_home(),
        section=get_section_body()
    )


def get_page_section_home_footer():
    return PageSection.objects.get(
        page=get_page_home(),
        section=get_section_footer()
    )


def get_page_section_information_body():
    return PageSection.objects.get(
        page=get_page_information(),
        section=get_section_body()
    )


def get_section_body():
    return Section.objects.get(slug='body')


def get_section_footer():
    return Section.objects.get(slug='footer')


def default_block_state():
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
    default_block_state()
    home = init_page('Home', 0, 'example/page_content.html')
    body = init_section('Body')
    init_page_section(
        home,
        body,
        'example',
        'Title',
        'example.title.create'
    )
    footer = init_section('Footer')
    init_page_section(
        home,
        footer,
        'example',
        'Title',
        'example.title.create'
    )
    information = init_page('Information', 1, 'example/page_content.html')
    init_page_section(
        information,
        body,
        'example',
        'Title',
        'example.title.create'
    )

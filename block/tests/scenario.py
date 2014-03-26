# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from block.models import (
    ADD,
    EDIT,
    EditState,
    ModerateState,
    Page,
    PENDING,
    PUBLISHED,
    PUSH,
    REMOVED,
    Section,
)
from block.service import init_page
from block.tests.model_maker import (
    make_edit_state,
    make_moderate_state,
    make_page,
    make_section,
)


def get_page_home():
    return Page.objects.get(slug='home')


def get_page_information():
    return Page.objects.get(slug='information')


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
    init_page('Home', 0)
    make_section('Body')
    make_section('Footer')
    init_page('Information', 1)

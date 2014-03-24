# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from block.models import (
    PENDING,
    PUBLISHED,
    REMOVED,
    ModerateState,
    Page,
    Section,
)
from block.tests.model_maker import (
    make_page,
    make_moderate_state,
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


def default_moderate_state():
    try:
        ModerateState.pending()
    except ModerateState.DoesNotExist:
        make_moderate_state(PENDING)
    try:
        ModerateState.objects.get(slug=PUBLISHED)
    except ModerateState.DoesNotExist:
        make_moderate_state(PUBLISHED)
    try:
        ModerateState.removed()
    except ModerateState.DoesNotExist:
        make_moderate_state(REMOVED)


def default_scenario_block():
    default_moderate_state()
    make_page('Home', 0)
    make_section('Body')
    make_section('Footer')
    make_page('Information', 1)

# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from block.models import (
    ModerateState,
    Page,
    Section,
)
from block.tests.model_maker import (
    make_page,
    make_moderate_state,
    make_section,
)


def get_layout_body():
    return Layout.objects.get(slug='body')


def get_layout_footer():
    return Layout.objects.get(slug='footer')


def get_page_information():
    return Page.objects.get(slug='information')


def get_page_home():
    return Page.objects.get(slug='home')


def get_section_home_body():
    return Section.objects.get(
        page=get_page_home(),
        layout=get_layout_body(),
    )


def get_section_home_footer():
    return Section.objects.get(
        page=get_page_home(),
        layout=get_layout_footer(),
    )


def get_section_information_body():
    return Section.objects.get(
        page=get_page_information(),
        layout=get_layout_body(),
    )


def default_moderate_state():
    try:
        ModerateState.pending()
    except ModerateState.DoesNotExist:
        make_moderate_state('pending')
    try:
        ModerateState.published()
    except ModerateState.DoesNotExist:
        make_moderate_state('published')
    try:
        ModerateState.removed()
    except ModerateState.DoesNotExist:
        make_moderate_state('removed')


def default_scenario_block():
    default_moderate_state()
    page = make_page('Home', 0)
    body = make_layout('Body')
    footer = make_layout('Footer')
    make_section(page, body)
    make_section(page, footer)
    page_info = make_page('Information', 1)
    make_section(page_info, body)

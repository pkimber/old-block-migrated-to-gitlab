# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from block.models import (
    ModerateState,
    Page,
)
from block.tests.model_maker import (
    make_page,
    make_moderate_state,
    make_section,
)


def get_page_information():
    return Page.objects.get(slug='information')


def get_page_home():
    return Page.objects.get(slug='home')


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
    make_page('Home', 0)
    make_section('Body')
    make_section('Footer')
    make_page('Information', 1)

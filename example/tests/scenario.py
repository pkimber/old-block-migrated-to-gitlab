# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from block.models import ModerateState
from block.tests.scenario import (
    default_moderate_state,
    default_scenario_block,
    get_page_home,
    get_page_information,
    get_section_body,
    get_section_footer,
)
from example.models import TestContent
from example.tests.model_maker import (
    make_test_block,
    make_test_content,
)


def get_block_hatherleigh_two():
    result = TestContent.objects.get(title='Hatherleigh Two')
    return result.block


def get_hatherleigh_old():
    return TestContent.objects.get(title='Hatherleigh Old')


def get_hatherleigh_two():
    return TestContent.objects.get(title='Hatherleigh Two')


def get_hatherleigh_three():
    return TestContent.objects.get(title='Hatherleigh Three')


def get_jacobstowe_one():
    return TestContent.objects.get(title='Jacobstowe One')


def get_monkokehampton():
    return TestContent.objects.get(title='Monkokehampton')


def default_scenario_project():
    default_moderate_state()
    default_scenario_block()
    # Home, Hatherleigh
    home = get_page_home()
    information = get_page_information()
    body = get_section_body()
    footer = get_section_footer()
    block_hatherleigh = make_test_block(home, body)
    make_test_content(
        block_hatherleigh,
        ModerateState.published(),
        1,
        'Hatherleigh Two'
    )
    make_test_content(
        block_hatherleigh,
        ModerateState.pending(),
        1,
        'Hatherleigh Three'
    )
    make_test_content(
        block_hatherleigh,
        ModerateState.removed(),
        1,
        'Hatherleigh Old'
    )
    # Home, Jacobstowe
    block_jacobstowe = make_test_block(home, body)
    make_test_content(
        block_jacobstowe,
        ModerateState.published(),
        2,
        'Jacobstowe One'
    )
    # Home, Footer
    block_jacobstowe = make_test_block(home, footer)
    make_test_content(
        block_jacobstowe,
        ModerateState.published(),
        1,
        'Villages for You'
    )
    # Information, Monkokehampton
    block_monkokehampton = make_test_block(information, body)
    make_test_content(
        block_monkokehampton,
        ModerateState.published(),
        1,
        'Monkokehampton'
    )

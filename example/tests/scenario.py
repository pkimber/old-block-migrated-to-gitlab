# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from block.models import (
    ModerateState,
    PENDING,
    PUBLISHED,
)
from block.tests.scenario import (
    default_moderate_state,
    default_scenario_block,
    get_page_home,
    get_page_information,
    get_section_body,
    get_section_footer,
)
from login.tests.scenario import get_user_staff

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


def get_jacobstowe_one_pending():
    return TestContent.objects.get(
        moderate_state__slug=PENDING,
        title='Jacobstowe One',
    )


def get_jacobstowe_one_published():
    return TestContent.objects.get(
        moderate_state__slug=PUBLISHED,
        title='Jacobstowe One',
    )


def get_monkokehampton():
    return TestContent.objects.get(title='Monkokehampton')


def default_scenario_example():
    default_moderate_state()
    default_scenario_block()
    # pages
    home = get_page_home()
    information = get_page_information()
    # sections
    body = get_section_body()
    footer = get_section_footer()
    # Home, Hatherleigh
    block_hatherleigh = make_test_block(home, body)
    c = make_test_content(
        block_hatherleigh,
        ModerateState.pending(),
        1,
        'Hatherleigh Two'
    )
    c.publish(get_user_staff())
    c.title = 'Hatherleigh Three'
    c.save()
    #make_test_content(
    #    block_hatherleigh,
    #    ModerateState.pending(),
    #    1,
    #    'Hatherleigh Three'
    #)
    make_test_content(
        block_hatherleigh,
        ModerateState.removed(),
        1,
        'Hatherleigh Old'
    )
    # Home, Jacobstowe
    block_jacobstowe = make_test_block(home, body)
    c = make_test_content(
        block_jacobstowe,
        ModerateState.pending(),
        2,
        'Jacobstowe One'
    )
    c.publish(get_user_staff())
    # Home, Footer
    block_jacobstowe = make_test_block(home, footer)
    c = make_test_content(
        block_jacobstowe,
        ModerateState.pending(),
        1,
        'Villages for You'
    )
    c.publish(get_user_staff())
    # Information, Monkokehampton
    block_monkokehampton = make_test_block(information, body)
    c = make_test_content(
        block_monkokehampton,
        ModerateState.pending(),
        1,
        'Monkokehampton'
    )
    c.publish(get_user_staff())

# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from block.models import (
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


def get_block_hatherleigh_old():
    return get_hatherleigh_old().block


def get_block_hatherleigh_three():
    return get_hatherleigh_three().block


def get_block_hatherleigh_two():
    return get_hatherleigh_two().block


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
    hatherleigh_body_1 = make_test_block(home, body)
    make_test_content(
        hatherleigh_body_1,
        1,
        'Hatherleigh Two'
    )
    hatherleigh_body_1.publish(get_user_staff())
    c = hatherleigh_body_1.get_pending()
    c.title = 'Hatherleigh Three'
    c.save()
    #make_test_content(
    #    block_hatherleigh,
    #    ModerateState.pending(),
    #    1,
    #    'Hatherleigh Three'
    #)
    hatherleigh_body_2 = make_test_block(home, body)
    make_test_content(
        hatherleigh_body_2,
        2,
        'Hatherleigh Old'
    )
    hatherleigh_body_2.remove(get_user_staff())
    # Home, Jacobstowe
    jacobstowe_body = make_test_block(home, body)
    make_test_content(
        jacobstowe_body,
        2,
        'Jacobstowe One'
    )
    jacobstowe_body.publish(get_user_staff())
    # Home, Footer
    jacobstowe_footer = make_test_block(home, footer)
    make_test_content(
        jacobstowe_footer,
        1,
        'Villages for You'
    )
    jacobstowe_footer.publish(get_user_staff())
    # Information, Monkokehampton
    monkokehampton_body = make_test_block(information, body)
    make_test_content(
        monkokehampton_body,
        1,
        'Monkokehampton'
    )
    monkokehampton_body.publish(get_user_staff())

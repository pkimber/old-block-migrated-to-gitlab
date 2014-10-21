# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from block.models import (
    PENDING,
    PUBLISHED,
)
from block.tests.scenario import (
    get_page_section_home_body,
    get_page_section_information_body,
)
from login.tests.scenario import get_user_staff

from example.models import Title
from example.tests.model_maker import (
    make_title,
    make_title_block,
)


def get_block_hatherleigh_old():
    return get_hatherleigh_old().block


def get_block_hatherleigh_three():
    return get_hatherleigh_three().block


def get_block_hatherleigh_two():
    return get_hatherleigh_two().block


def get_hatherleigh_old():
    return Title.objects.get(title='Hatherleigh Old')


def get_hatherleigh_two():
    return Title.objects.get(title='Hatherleigh Two')


def get_hatherleigh_three():
    return Title.objects.get(title='Hatherleigh Three')


def get_jacobstowe_one_pending():
    return Title.objects.get(
        moderate_state__slug=PENDING,
        title='Jacobstowe One',
    )


def get_jacobstowe_one_published():
    return Title.objects.get(
        moderate_state__slug=PUBLISHED,
        title='Jacobstowe One',
    )


def get_monkokehampton():
    return Title.objects.get(title='Monkokehampton')


def default_scenario_example():
    # page sections
    home_body = get_page_section_home_body()
    information_body = get_page_section_information_body()
    # Home, Hatherleigh
    hatherleigh_body_1 = make_title_block(home_body)
    make_title(
        hatherleigh_body_1,
        1,
        'Hatherleigh Two'
    )
    hatherleigh_body_1.publish(get_user_staff())
    c = hatherleigh_body_1.get_pending()
    c.title = 'Hatherleigh Three'
    c.save()
    hatherleigh_body_2 = make_title_block(home_body)
    make_title(
        hatherleigh_body_2,
        2,
        'Hatherleigh Old'
    )
    hatherleigh_body_2.remove(get_user_staff())
    # Home, Jacobstowe
    jacobstowe_body = make_title_block(home_body)
    make_title(
        jacobstowe_body,
        2,
        'Jacobstowe One'
    )
    jacobstowe_body.publish(get_user_staff())
    # Information, Monkokehampton
    monkokehampton_body = make_title_block(information_body)
    make_title(
        monkokehampton_body,
        1,
        'Monkokehampton'
    )
    monkokehampton_body.publish(get_user_staff())

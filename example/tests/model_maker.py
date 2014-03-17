# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from base.tests.model_maker import clean_and_save

from example.models import (
    TestBlock,
    TestBlockContent,
    TestContent,
)


def make_test_block(page, section, **kwargs):
    defaults = dict(
        page=page,
        section=section,
    )
    defaults.update(kwargs)
    return clean_and_save(TestBlock(**defaults))


def make_test_block_content(block, moderate_state, order, title, **kwargs):
    defaults = dict(
        block=block,
        moderate_state=moderate_state,
        order=order,
        title=title,
    )
    defaults.update(kwargs)
    return clean_and_save(TestBlockContent(**defaults))


def make_test_content(container, moderate_state, title, **kwargs):
    defaults = dict(
        container=container,
        moderate_state=moderate_state,
        title=title,
    )
    defaults.update(kwargs)
    return clean_and_save(TestContent(**defaults))

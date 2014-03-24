# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from base.tests.model_maker import clean_and_save

from example.models import (
    TestBlock,
    TestContent,
)


def make_test_block(page, section, **kwargs):
    defaults = dict(
        page=page,
        section=section,
    )
    defaults.update(kwargs)
    return clean_and_save(TestBlock(**defaults))


def make_test_content(block, order, title, **kwargs):
    defaults = dict(
        block=block,
        order=order,
        title=title,
    )
    defaults.update(kwargs)
    return clean_and_save(TestContent(**defaults))

# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from base.tests.model_maker import clean_and_save

from example.models import (
    Title,
    TitleBlock,
)


def make_title_block(page, section, **kwargs):
    defaults = dict(
        page=page,
        section=section,
    )
    defaults.update(kwargs)
    return clean_and_save(TitleBlock(**defaults))


def make_title(block, order, title, **kwargs):
    defaults = dict(
        block=block,
        order=order,
        title=title,
    )
    defaults.update(kwargs)
    return clean_and_save(Title(**defaults))

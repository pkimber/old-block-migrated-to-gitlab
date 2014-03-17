# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from base.tests.model_maker import clean_and_save

from example.models import TestContent


def make_test_content(container, moderate_state, title, **kwargs):
    defaults = dict(
        container=container,
        moderate_state=moderate_state,
        title=title,
    )
    defaults.update(kwargs)
    return clean_and_save(TestContent(**defaults))

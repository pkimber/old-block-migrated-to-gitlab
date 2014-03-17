# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.text import slugify

from base.tests.model_maker import clean_and_save

from block.models import (
    Container,
    Layout,
    ModerateState,
    Page,
    Section,
)


def make_container(section, order, **kwargs):
    defaults = dict(
        section=section,
        order=order,
    )
    defaults.update(kwargs)
    return clean_and_save(Container(**defaults))


def make_moderate_state(name, **kwargs):
    defaults = dict(
        name=name,
        slug=slugify(name),
    )
    defaults.update(kwargs)
    return clean_and_save(ModerateState(**defaults))


def make_page(name, order, **kwargs):
    defaults = dict(
        name=name,
        order=order,
        slug=slugify(name),
    )
    defaults.update(kwargs)
    return clean_and_save(Page(**defaults))


def make_section(page, layout, **kwargs):
    defaults = dict(
        page=page,
        layout=layout,
    )
    defaults.update(kwargs)
    return clean_and_save(Section(**defaults))


def make_layout(name, **kwargs):
    defaults = dict(
        name=name,
        slug=slugify(name),
    )
    defaults.update(kwargs)
    return clean_and_save(Layout(**defaults))

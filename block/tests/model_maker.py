# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.text import slugify

from base.tests.model_maker import clean_and_save

from block.models import (
    EditState,
    ModerateState,
    Page,
    PageSection,
    Section,
)


def make_edit_state(name, **kwargs):
    defaults = dict(
        name=name,
        slug=slugify(name),
    )
    defaults.update(kwargs)
    return clean_and_save(EditState(**defaults))


def make_moderate_state(name, **kwargs):
    defaults = dict(
        name=name,
        slug=slugify(name),
    )
    defaults.update(kwargs)
    return clean_and_save(ModerateState(**defaults))


def make_page(name, order, template_name, **kwargs):
    defaults = dict(
        name=name,
        order=order,
        slug=slugify(name),
        template_name=template_name,
    )
    defaults.update(kwargs)
    return clean_and_save(Page(**defaults))


def make_page_section(page, section, block_app, block_model, create_url_name):
    defaults = dict(
        page=page,
        section=section,
        block_app=block_app,
        block_model=block_model,
        create_url_name=create_url_name,
    )
    return clean_and_save(PageSection(**defaults))


def make_section(name, **kwargs):
    defaults = dict(
        name=name,
        slug=slugify(name),
    )
    defaults.update(kwargs)
    return clean_and_save(Section(**defaults))

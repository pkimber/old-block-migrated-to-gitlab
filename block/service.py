# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.text import slugify

from block.models import (
    Page,
    PageSection,
    Section,
)
from block.tests.model_maker import (
    make_page,
    make_page_section,
    make_section,
)


def init_section(name):
    """Create a section if it doesn't already exist."""
    try:
        result = Section.objects.get(slug=slugify(name))
    except Section.DoesNotExist:
        result = make_section(name)
    return result


def init_page(name, order, template_name, is_home=None, slug_menu=None):
    """Create a page if it doesn't already exist."""
    if not is_home:
        is_home = False
    if not slug_menu:
        slug_menu = ''
    try:
        result = Page.objects.get(
            slug=slugify(name),
            slug_menu=slugify(slug_menu),
        )
        update = False
        if order != result.order:
            result.order = order
            update = True
        if is_home != result.is_home:
            result.is_home = is_home
            update = True
        if template_name != result.template_name:
            result.template_name = template_name
            update = True
        if update:
            result.save()
    except Page.DoesNotExist:
        result = make_page(
            name,
            order,
            is_home=is_home,
            template_name=template_name,
            slug_menu=slugify(slug_menu),
        )
    return result


def init_page_section(page, section, block_app, block_model, url_name):
    try:
        result = PageSection.objects.get(page=page, section=section)
        update = False
        if block_app != result.block_app:
            result.block_app = block_app
            update = True
        if block_model != result.block_model:
            result.block_model = block_model
            update = True
        if url_name != result.url_name:
            result.url_name = url_name
            update = True
        if update:
            result.save()
    except PageSection.DoesNotExist:
        result = make_page_section(
            page,
            section,
            block_app,
            block_model,
            url_name,
        )
    return result

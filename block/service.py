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


def init_section(name, block_app, block_model, create_url_name, paginated=None):
    """Create a section if it doesn't already exist."""
    if not create_url_name:
        create_url_name = ''
    try:
        result = Section.objects.get(slug=slugify(name))
        update = False
        if block_app != result.block_app:
            result.block_app = block_app
            update = True
        if block_model != result.block_model:
            result.block_model = block_model
            update = True
        if create_url_name != result.create_url_name:
            result.create_url_name = create_url_name
            update = True
        if ((paginated and not result.paginated)
          or (not paginated and result.paginated)
          or (paginated and result.paginated
            and (paginated.items_per_page != result.paginated.items_per_page or
            paginated.order_by_field != result.paginated.order_by_field))):
            if (result.paginated):
                result.paginated.items_per_page = paginated.items_per_page
                result.paginated.order_by_field = paginated.order_by_field
            else:
                result.paginated = paginated
            result.paginated.save()
            update = True
        if update:
            result.save()
    except Section.DoesNotExist:
        result = make_section(
            name,
            block_app,
            block_model,
            create_url_name,
            paginated=paginated
        )
    return result


def init_page(
        name, slug_page, order, template_name, is_home=None, slug_menu=None):
    """Create a page if it doesn't already exist."""
    if not is_home:
        is_home = False
    if not slug_menu:
        slug_menu = ''
    try:
        result = Page.objects.get(
            slug=slug_page,
            slug_menu=slugify(slug_menu),
        )
        update = False
        if name != result.name:
            result.name = name
            update = True
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
            slug_page,
            order,
            is_home=is_home,
            template_name=template_name,
            slug_menu=slugify(slug_menu),
        )
    return result


def init_page_section(page, section):
    try:
        result = PageSection.objects.get(page=page, section=section)
    except PageSection.DoesNotExist:
        result = make_page_section(page, section)
    return result

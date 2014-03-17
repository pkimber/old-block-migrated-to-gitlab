# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.text import slugify

from block.models import (
    Container,
    Layout,
    Page,
    Section,
)
from block.tests.model_maker import (
    make_container,
    make_layout,
    make_page,
    make_section,
)


def init_container(section, order):
    """Create a footer - if there isn't one already."""
    result = Container.objects.filter(section=section)
    if result:
        return result[0]
    else:
        return make_container(section, order)


def init_layout(name):
    """Create a layout if it doesn't already exist."""
    try:
        result = Layout.objects.get(slug=slugify(name))
    except Layout.DoesNotExist:
        result = make_layout(name)
    return result


def init_page(name, order, is_home=None):
    """Create a page if it doesn't already exist."""
    if not is_home:
        is_home = False
    try:
        result = Page.objects.get(slug=slugify(name))
        update = False
        if order != result.order:
            result.order = order
            update = True
        if is_home != result.is_home:
            result.is_home = is_home
            update = True
        if update:
            result.save()
    except Page.DoesNotExist:
        result = make_page(name, order, is_home=is_home)
    return result


def init_section(page, layout):
    try:
        result = Section.objects.get(page=page, layout=layout)
    except Section.DoesNotExist:
        result = make_section(page, layout)
    return result

# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.text import slugify

from block.models import (
    Page,
    Section,
)
from block.tests.model_maker import (
    make_page,
    make_section,
)


def init_section(name):
    """Create a section if it doesn't already exist."""
    try:
        result = Section.objects.get(slug=slugify(name))
    except Section.DoesNotExist:
        result = make_section(name)
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

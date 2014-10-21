# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django import template


register = template.Library()


@register.inclusion_tag('block/_add.html')
def block_add(url):
    return dict(url=url)


@register.inclusion_tag('block/_moderate.html')
def block_moderate(generic_content, can_remove=True):
    return dict(c=generic_content, can_remove=can_remove)


@register.inclusion_tag('block/_status.html')
def block_status(generic_content):
    return dict(c=generic_content)

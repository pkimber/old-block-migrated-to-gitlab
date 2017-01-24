# -*- encoding: utf-8 -*-
from django import template

register = template.Library()


@register.inclusion_tag('block/_add.html')
def block_add(url, caption="", return_path=None):
    return dict(url=url, caption=caption, return_path=return_path)


@register.inclusion_tag('block/_moderate.html')
def block_moderate(
        generic_content, can_remove=True, caption="", return_path=None):
    return dict(
        c=generic_content, can_remove=can_remove, caption=caption,
        return_path=return_path
    )


@register.inclusion_tag('block/_status.html')
def block_status(generic_content):
    return dict(c=generic_content)

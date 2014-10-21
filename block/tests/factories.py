# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import factory

from block.models import Page


class PageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Page

    @factory.sequence
    def slug(n):
        return 'page_{:02d}'.format(n)

    @factory.sequence
    def slug_menu(n):
        return 'menu_{:02d}'.format(n)

    @factory.sequence
    def template_name(n):
        return 'example/template_{:02d}.html'.format(n)

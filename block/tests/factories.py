# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import factory

from django.template.defaultfilters import slugify

from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from block.models import Page


class PageFactory(DjangoModelFactory):

    class Meta:
        model = Page

    slug = slugify(factory.Sequence(lambda n: 'page{}'.format(n)))
    slug_menu = slugify(factory.LazyAttribute(lambda o: '{}_menu'.format(o.slug)))

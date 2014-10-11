# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import factory

from block.models import PageSectionFactory
from example.models import (
    Title,
    TitleBlock,
)


class TitleBlockFactory(factory.django.DjangoModelFactory):

    page_section = PageSectionFactory()

    class Meta:
        model = TitleBlock


class TitleFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Title

    block = factory.SubFactory(TitleBlockFactory)

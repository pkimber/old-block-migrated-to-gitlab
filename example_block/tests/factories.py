# -*- encoding: utf-8 -*-
import factory

from block.tests.factories import PageSectionFactory
from example_block.models import (
    Title,
    TitleBlock,
)


class TitleBlockFactory(factory.django.DjangoModelFactory):

    page_section = factory.SubFactory(PageSectionFactory)

    class Meta:
        model = TitleBlock


class TitleFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Title

    block = factory.SubFactory(TitleBlockFactory)

    @factory.sequence
    def order(n):
        return n

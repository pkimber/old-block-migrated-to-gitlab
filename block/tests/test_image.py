# -*- encoding: utf-8 -*-
import pytest

from block.models import Image
from block.tests.factories import ImageCategoryFactory, ImageFactory


@pytest.mark.django_db
def test_image_factory():
    ImageFactory()


@pytest.mark.django_db
def test_image_str():
    str(ImageFactory())


@pytest.mark.django_db
def test_tags_by_category():
    category = ImageCategoryFactory()
    i1 = ImageFactory(category=category)
    i1.tags.add('a')
    i2 = ImageFactory(category=category)
    i2.tags.add('b')
    i3 = ImageFactory(category=category)
    i3.tags.add('b')
    qs = Image.objects.tags_by_category(category)
    assert [('b', 2), ('a', 1)] == [(x.slug, x.num_tags) for x in qs]

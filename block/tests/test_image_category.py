# -*- encoding: utf-8 -*-
import pytest

from block.models import ImageCategory
from block.tests.factories import ImageCategoryFactory
from block.tests.factories import ImageFactory


@pytest.mark.django_db
def test_categories():
    c1 = ImageCategoryFactory(slug='a')
    ImageCategoryFactory(slug='b', deleted=True)
    c3 = ImageCategoryFactory(slug='c')
    result = [c.slug for c in ImageCategory.objects.categories()]
    assert [c1.slug, c3.slug] == result


@pytest.mark.django_db
def test_in_use():
    c = ImageCategoryFactory()
    ImageFactory(category=c)
    assert c.in_use is True


@pytest.mark.django_db
def test_in_use_deleted():
    c = ImageCategoryFactory()
    ImageFactory(category=c, deleted=True)
    assert c.in_use is False


@pytest.mark.django_db
def test_in_use_not():
    c = ImageCategoryFactory()
    assert c.in_use is False

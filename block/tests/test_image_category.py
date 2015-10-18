# -*- encoding: utf-8 -*-
import pytest

from block.models import ImageCategory
from block.tests.factories import ImageCategoryFactory


@pytest.mark.django_db
def test_categories():
    c1 = ImageCategoryFactory(slug='a')
    c2 = ImageCategoryFactory(slug='b', deleted=True)
    c3 = ImageCategoryFactory(slug='c')
    result = [c.slug for c in ImageCategory.objects.categories()]
    assert [c1.slug, c3.slug] == result

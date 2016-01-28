# -*- encoding: utf-8 -*-
import pytest

from block.models import (
    Link,
    LinkCategory,
)
from block.tests.factories import LinkCategoryFactory
from block.tests.factories import LinkFactory


@pytest.mark.django_db
def test_categories():
    c1 = LinkCategoryFactory(slug='a')
    LinkCategoryFactory(slug='b', deleted=True)
    c3 = LinkCategoryFactory(slug='c')
    result = [c.slug for c in LinkCategory.objects.categories()]
    assert [c1.slug, c3.slug] == result


@pytest.mark.django_db
def test_in_use():
    c = LinkCategoryFactory()
    LinkFactory(category=c)
    assert c.in_use is True


@pytest.mark.django_db
def test_in_use_deleted():
    c = LinkCategoryFactory()
    LinkFactory(category=c, deleted=True)
    assert c.in_use is False


@pytest.mark.django_db
def test_in_use_not():
    c = LinkCategoryFactory()
    assert c.in_use is False

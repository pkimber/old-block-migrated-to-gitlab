# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

from block.models import BlockError
from block.tests.factories import (
    ImageCategoryFactory,
    ImageFactory,
)
from login.tests.factories import (
    TEST_PASSWORD,
    UserFactory,
)


@pytest.mark.django_db
def test_category_delete(client):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    category = ImageCategoryFactory()
    assert category.deleted is False
    # test
    url = reverse('block.image.category.delete', args=[category.pk])
    response = client.post(url)
    # check
    assert 302 == response.status_code
    expect = reverse('block.image.category.list')
    assert expect in response['Location']
    category.refresh_from_db()
    assert category.deleted is True


@pytest.mark.django_db
def test_category_delete_exception(client):
    """Should not delete a category which is in use."""
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    category = ImageCategoryFactory()
    image = ImageFactory(category=category)
    assert category.deleted is False
    # test
    url = reverse('block.image.category.delete', args=[category.pk])
    with pytest.raises(BlockError) as e:
        client.post(url)
    assert 'Cannot delete an image category which is in use' in str(e.value)

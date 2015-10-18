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


@pytest.mark.django_db
def test_category_update(client):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    category = ImageCategoryFactory()
    url = reverse('block.image.category.update', args=[category.pk])
    data = {
        'name': 'Cricket',
    }
    response = client.post(url, data)
    # check
    assert 302 == response.status_code
    expect = reverse('block.image.category.list')
    assert expect in response['Location']
    category.refresh_from_db()
    assert 'Cricket' == category.name


@pytest.mark.django_db
def test_image_update(client):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    image = ImageFactory()
    url = reverse('block.image.update', args=[image.pk])
    data = {
        'title': 'Football',
    }
    response = client.post(url, data)
    # check
    assert 302 == response.status_code
    expect = reverse('block.image.list')
    assert expect in response['Location']
    image.refresh_from_db()
    assert 'Football' == image.title

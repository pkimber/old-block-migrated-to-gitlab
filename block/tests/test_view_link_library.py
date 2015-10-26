# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

from block.models import (
    BlockError,
    Link,
)
from block.tests.factories import (
    LinkCategory,
    LinkCategoryFactory,
    LinkFactory,
)
from login.tests.factories import (
    TEST_PASSWORD,
    UserFactory,
)


@pytest.mark.django_db
def test_category_create(client):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = reverse('block.link.category.create')
    data = {
        'name': 'Tennis',
    }
    response = client.post(url, data)
    # check
    assert 302 == response.status_code
    expect = reverse('block.link.category.list')
    assert expect in response['Location']
    categories = LinkCategory.objects.all()
    assert 1 == categories.count()
    assert 'Tennis' == categories[0].name


@pytest.mark.django_db
def test_category_delete(client):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    category = LinkCategoryFactory()
    assert category.deleted is False
    # test
    url = reverse('block.link.category.delete', args=[category.pk])
    response = client.post(url)
    # check
    assert 302 == response.status_code
    expect = reverse('block.link.category.list')
    assert expect in response['Location']
    category.refresh_from_db()
    assert category.deleted is True


@pytest.mark.django_db
def test_category_delete_exception(client):
    """Should not delete a category which is in use."""
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    category = LinkCategoryFactory()
    LinkFactory(category=category)
    assert category.deleted is False
    # test
    url = reverse('block.link.category.delete', args=[category.pk])
    with pytest.raises(BlockError) as e:
        client.post(url)
    assert 'Cannot delete a link category which is in use' in str(e.value)


@pytest.mark.django_db
def test_category_update(client):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    category = LinkCategoryFactory()
    url = reverse('block.link.category.update', args=[category.pk])
    data = {
        'name': 'Cricket',
    }
    response = client.post(url, data)
    # check
    assert 302 == response.status_code
    expect = reverse('block.link.category.list')
    assert expect in response['Location']
    category.refresh_from_db()
    assert 'Cricket' == category.name


#@pytest.mark.django_db
#def test_link_delete(client):
#    user = UserFactory(is_staff=True)
#    assert client.login(username=user.username, password=TEST_PASSWORD) is True
#    link_1 = LinkFactory()
#    link_2 = LinkFactory()
#    link_3 = LinkFactory()
#    url = reverse('block.link.list.delete')
#    data = {
#        'links': [link_1.pk, link_3.pk],
#    }
#    response = client.post(url, data)
#    # check
#    assert 302 == response.status_code
#    expect = reverse('block.link.list')
#    assert expect in response['Location']
#    result = [link.pk for link in Link.objects.links()]
#    assert [link_2.pk] == result


#@pytest.mark.django_db
#def test_link_update(client):
#    user = UserFactory(is_staff=True)
#    assert client.login(username=user.username, password=TEST_PASSWORD) is True
#    link = LinkFactory()
#    url = reverse('block.link.update', args=[link.pk])
#    data = {
#        'title': 'Football',
#    }
#    response = client.post(url, data)
#    # check
#    assert 302 == response.status_code
#    expect = reverse('block.link.list')
#    assert expect in response['Location']
#    link.refresh_from_db()
#    assert 'Football' == link.title

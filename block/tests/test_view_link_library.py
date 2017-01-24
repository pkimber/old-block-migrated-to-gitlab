# -*- encoding: utf-8 -*-
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse

from block.models import (
    BlockError,
    Document,
    Link,
    Url,
)
from block.tests.factories import (
    DocumentFactory,
    LinkCategory,
    LinkCategoryFactory,
    LinkFactory,
    PageFactory,
    UrlFactory,
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


@pytest.mark.django_db
def test_link_delete(client):
    user = UserFactory(is_staff=True)
    assert client.login(
        username=user.username, password=TEST_PASSWORD
    ) is True
    link_1 = LinkFactory()
    link_2 = LinkFactory()
    link_3 = LinkFactory()
    url = reverse('block.link.delete', args=[link_2.pk])
    data = {}
    response = client.post(url, data)
    # check
    assert 302 == response.status_code
    expect = reverse('block.link.list')
    assert expect in response['Location']
    result = [link.pk for link in Link.objects.links()]
    assert [link_1.pk, link_3.pk] == result


@pytest.mark.django_db
def test_link_external_update(client):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    link = LinkFactory(link_type='u', url_external="https://google.com")
    url = reverse('block.link.external.update', args=[link.pk])
    data = {
        'title': 'Football',
        'url_external': 'http://www.bbc.co.uk/sport/football'
    }
    response = client.post(url, data)
    # check
    assert 302 == response.status_code
    expect = reverse('block.link.list')
    assert expect in response['Location']
    link.refresh_from_db()
    assert 'Football' == link.title
    assert 'http://www.bbc.co.uk/sport/football' == link.url


@pytest.mark.django_db
def test_link_internal_update(client):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    link = LinkFactory(link_type='r', url_internal=UrlFactory())
    url = reverse('block.link.internal.update', args=[link.pk])
    page = PageFactory(slug='football', slug_menu='')
    new_url = UrlFactory(url_type=Url.PAGE, page=page)
    data = {
        'title': 'Football',
        'url_internal': new_url.pk
    }
    response = client.post(url, data)
    # check
    assert 302 == response.status_code
    expect = reverse('block.link.list')
    assert expect in response['Location']
    link.refresh_from_db()
    assert 'Football' == link.title
    assert '/football/' == link.url


def test_file():
    """create a file ready to upload."""
    return SimpleUploadedFile.from_dict(
        dict(filename='test.txt', content=bytes('abc', 'UTF-8'))
    )


@pytest.mark.django_db
def test_link_document_create(client):
    category = LinkCategoryFactory()
    DocumentFactory()
    # image = ImageFactory()
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = reverse('block.link.document.create')
    # create a document ready to upload
    data = {
        'category': category.pk,
        'document': test_file(),
        'title': 'Cricket',
    }
    response = client.post(url, data)
    # check
    expect = reverse('block.link.list')
    assert 302 == response.status_code
    assert expect in response['Location']
    link = Link.objects.get(title='Cricket')
    assert 'Cricket' == link.title
    assert category == link.category
    assert link.document.deleted is False
    # check a document has been added to the database
    assert 2 == Document.objects.count()


@pytest.mark.django_db
def test_link_document_update(client):
    category = LinkCategoryFactory()
    DocumentFactory()
    link = LinkFactory(link_type=Link.DOCUMENT, document=DocumentFactory())
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = reverse('block.link.document.update', args=[link.pk])
    # create a document ready to upload
    data = {
        'category': category.pk,
        'document': test_file(),
        'title': 'Cricket',
    }
    response = client.post(url, data)
    # check
    expect = reverse('block.link.list')
    assert 302 == response.status_code
    assert expect in response['Location']
    link = Link.objects.get(title='Cricket')
    assert 'Cricket' == link.title
    assert category == link.category
    assert 'test.txt' == link.file_name
    assert link.document.deleted is False
    # test for partial name only
    assert "/media/link/document/test" in link.url
    # check a document has been added to the database
    assert 2 == Document.objects.count()


@pytest.mark.django_db
def test_link_redirect(client):
    ext_url = "http://example.com"
    link = LinkFactory(link_type=Link.URL_EXTERNAL, url_external=ext_url)
    user = UserFactory()
    assert client.login(username=user.username, password=TEST_PASSWORD)
    url = reverse('block.link.follow', args=[link.link_type, link.pk])
    response = client.get(url)
    # check
    assert 302 == response.status_code
    assert ext_url in response['Location']


@pytest.mark.django_db
def test_link_redirect_invalid(client):
    ext_url = "http://example.com"
    link = LinkFactory(link_type=Link.URL_EXTERNAL, url_external=ext_url)
    user = UserFactory()
    assert client.login(username=user.username, password=TEST_PASSWORD)
    # type should be 'u' in this case so 'd' will raise a 404
    url = reverse('block.link.follow', args=['d', link.pk])
    response = client.get(url)
    # check
    assert 404 == response.status_code

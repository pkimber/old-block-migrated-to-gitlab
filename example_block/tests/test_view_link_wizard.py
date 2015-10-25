# -*- encoding: utf-8 -*-
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from block.models import (
    Document,
    Link,
    Url,
    Wizard,
)
from block.tests.factories import (
    DocumentFactory,
    LinkCategoryFactory,
    LinkFactory,
    PageFactory,
    UrlFactory,
)
from example_block.tests.factories import TitleFactory
from example_block.tests.test_view_perm import (
    url_link_multi,
    url_link_single,
)
from login.tests.factories import (
    TEST_PASSWORD,
    UserFactory,
)
from login.tests.fixture import perm_check


def test_file():
    """create a file ready to upload."""
    return SimpleUploadedFile.from_dict(
        dict(filename='test.txt', content=bytes('abc', 'UTF-8'))
    )


@pytest.mark.django_db
def test_perm(perm_check):
    urls = TitleFactory().wizard_urls
    url = next(x['url'] for x in urls if 'Link' in x['caption'])
    perm_check.staff(url)


@pytest.mark.django_db
def test_choose_multi(client):
    content = TitleFactory()
    link_1 = LinkFactory(link_type=Link.URL_EXTERNAL)
    link_2 = LinkFactory(link_type=Link.URL_EXTERNAL)
    user = UserFactory(is_staff=True)
    assert 0 == content.references.count()
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = url_link_multi(content, 'block.wizard.link.choose')
    data = {
        'links': [link_2.pk, link_1.pk],
    }
    response = client.post(url, data)
    # check
    assert 302 == response.status_code
    expect = url_link_multi(content, 'block.wizard.link.option')
    assert expect in response['Location']
    content.refresh_from_db()
    assert 2 == content.references.count()
    # ordering controlled by 'ordering' on 'TitleReference' model
    assert [1, 2] == [item.order for item in content.ordered_references()]


@pytest.mark.django_db
def test_choose_category_multi(client):
    """Choose from links in the selected category."""
    content = TitleFactory()
    category = LinkCategoryFactory()
    LinkFactory(link_type=Link.URL_EXTERNAL)
    link_2 = LinkFactory(category=category, link_type=Link.URL_EXTERNAL)
    LinkFactory(link_type=Link.URL_EXTERNAL)
    link_4 = LinkFactory(category=category, link_type=Link.URL_EXTERNAL)
    user = UserFactory(is_staff=True)
    assert 0 == content.references.count()
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = url_link_multi(content, 'block.wizard.link.choose', category=category)
    assert category.slug in url
    data = {
        'links': [link_2.pk, link_4.pk],
    }
    response = client.post(url, data)
    # check
    assert 302 == response.status_code
    expect = url_link_multi(content, 'block.wizard.link.option')
    assert expect in response['Location']
    content.refresh_from_db()
    assert 2 == content.references.count()
    # ordering controlled by 'ordering' on 'TitleReference' model
    assert [1, 2] == [item.order for item in content.ordered_references()]


@pytest.mark.django_db
def test_choose_single(client):
    content = TitleFactory()
    LinkFactory(link_type=Link.URL_EXTERNAL)
    link = LinkFactory(link_type=Link.URL_EXTERNAL)
    user = UserFactory(is_staff=True)
    assert content.link is None
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = url_link_single(content, 'block.wizard.link.choose')
    data = {
        'links': link.pk,
    }
    response = client.post(url, data)
    # check
    assert 302 == response.status_code
    expect = content.block.page_section.page.get_design_url()
    assert expect in response['Location']
    content.refresh_from_db()
    assert link == content.link


@pytest.mark.django_db
def test_choose_single_category(client):
    """Choose from links in the selected category."""
    content = TitleFactory()
    category = LinkCategoryFactory()
    LinkFactory(link_type=Link.URL_EXTERNAL)
    link = LinkFactory(category=category, link_type=Link.URL_EXTERNAL)
    user = UserFactory(is_staff=True)
    assert content.link is None
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = url_link_single(content, 'block.wizard.link.choose', category=category)
    assert category.slug in url
    data = {
        'links': link.pk,
    }
    response = client.post(url, data)
    # check
    assert 302 == response.status_code
    expect = content.block.page_section.page.get_design_url()
    assert expect in response['Location']
    content.refresh_from_db()
    assert link == content.link


@pytest.mark.django_db
def test_page_single(client):
    content = TitleFactory()
    #category = ImageCategoryFactory()
    page = PageFactory(name='Information', slug='info', slug_menu='')
    url_internal = Url.objects.init_page_url(page)
    user = UserFactory(is_staff=True)
    assert content.link is None
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = url_link_single(content, 'block.wizard.link.page')
    # create a document ready to upload
    data = {
        #'add_to_library': True,
        #'category': category.pk,
        'url_internal': url_internal.pk,
        'title': 'Cricket',
    }
    response = client.post(url, data)
    # check
    content.refresh_from_db()
    expect = content.block.page_section.page.get_design_url()
    assert 302 == response.status_code
    assert expect in response['Location']
    assert 'Cricket' == content.link.title
    assert url_internal == content.link.url_internal


@pytest.mark.django_db
def test_external_single(client):
    content = TitleFactory()
    #category = ImageCategoryFactory()
    #DocumentFactory()
    #image = ImageFactory()
    user = UserFactory(is_staff=True)
    assert content.link is None
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = url_link_single(content, 'block.wizard.link.external')
    # create a document ready to upload
    data = {
        'add_to_library': True,
        #'category': category.pk,
        'url_external': 'https://www.pkimber.net',
        'title': 'Rugby',
    }
    response = client.post(url, data)
    # check
    content.refresh_from_db()
    expect = content.block.page_section.page.get_design_url()
    assert 302 == response.status_code
    assert expect in response['Location']
    assert 'Rugby' == content.link.title
    assert content.link is not None
    assert 'https://www.pkimber.net' == content.link.url_external
    #assert content.link.category == category
    #assert content.link.document.deleted is False
    # check a document has been added to the database
    #assert 2 == Document.objects.count()


@pytest.mark.django_db
def test_remove_single(client):
    """The multi test for removing is ````."""
    link = LinkFactory(link_type=Link.URL_EXTERNAL)
    content = TitleFactory(link=link)
    user = UserFactory(is_staff=True)
    assert content.link is not None
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = url_link_single(content, 'block.wizard.link.remove')
    response = client.post(url)
    # check
    content.refresh_from_db()
    expect = content.block.page_section.page.get_design_url()
    assert 302 == response.status_code
    assert expect in response['Location']
    assert content.link is None


@pytest.mark.django_db
def test_upload_single(client):
    content = TitleFactory()
    category = LinkCategoryFactory()
    DocumentFactory()
    #image = ImageFactory()
    user = UserFactory(is_staff=True)
    assert content.link is None
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = url_link_single(content, 'block.wizard.link.upload')
    # create a document ready to upload
    data = {
        'add_to_library': True,
        'category': category.pk,
        'image': test_file(),
        'title': 'Cricket',
    }
    response = client.post(url, data)
    # check
    content.refresh_from_db()
    expect = content.block.page_section.page.get_design_url()
    assert 302 == response.status_code
    assert expect in response['Location']
    assert 'Cricket' == content.link.title
    assert content.link is not None
    assert category == content.link.category
    assert content.link.document.deleted is False
    # check a document has been added to the database
    assert 2 == Document.objects.count()

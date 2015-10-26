# -*- encoding: utf-8 -*-
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from block.models import (
    BlockError,
    Document,
    Link,
    Url,
)
from block.tests.factories import (
    DocumentFactory,
    LinkCategoryFactory,
    LinkFactory,
    PageFactory,
)
from example_block.tests.factories import (
    TitleFactory,
    TitleLinkFactory,
)
from example_block.tests.test_view_perm import (
    url_link_multi,
    url_link_single,
)
from login.tests.factories import (
    TEST_PASSWORD,
    UserFactory,
)


def test_file():
    """create a file ready to upload."""
    return SimpleUploadedFile.from_dict(
        dict(filename='test.txt', content=bytes('abc', 'UTF-8'))
    )


@pytest.mark.django_db
def test_choose_multi(client):
    content = TitleFactory()
    link_1 = LinkFactory()
    link_2 = LinkFactory()
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
    LinkFactory()
    link_2 = LinkFactory(category=category)
    LinkFactory()
    link_4 = LinkFactory(category=category)
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
    LinkFactory()
    link = LinkFactory()
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
    LinkFactory()
    link = LinkFactory(category=category)
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
    link = LinkFactory()
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


def _set_up_order_multi(content):
    link_1 = LinkFactory()
    link_2 = LinkFactory()
    link_3 = LinkFactory()
    link_4 = LinkFactory()
    t1 = TitleLinkFactory(content=content, link=link_1, order=1)
    t2 = TitleLinkFactory(content=content, link=link_2, order=2)
    t3 = TitleLinkFactory(content=content, link=link_3, order=3)
    t4 = TitleLinkFactory(content=content, link=link_4, order=4)
    return t1, t2, t3, t4


def _post_multi_order(client, content, data):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = url_link_multi(content, 'block.wizard.link.order')
    response = client.post(url, data)
    # check
    assert 302 == response.status_code
    assert url in response['Location']


@pytest.mark.django_db
def test_order_multi_down_1(client):
    content = TitleFactory()
    t1, t2, t3, t4 = _set_up_order_multi(content)
    _post_multi_order(client, content, {'down': t1.pk})
    assert [
        t2.pk, t1.pk, t3.pk, t4.pk
    ] == [item.pk for item in content.ordered_references()]


@pytest.mark.django_db
def test_order_multi_down_2(client):
    content = TitleFactory()
    t1, t2, t3, t4 = _set_up_order_multi(content)
    _post_multi_order(client, content, {'down': t2.pk})
    assert [
        t1.pk, t3.pk, t2.pk, t4.pk
    ] == [item.pk for item in content.ordered_references()]


@pytest.mark.django_db
def test_order_multi_down_4(client):
    """Trying to move the last item down, should raise an exception."""
    content = TitleFactory()
    t1, t2, t3, t4 = _set_up_order_multi(content)
    with pytest.raises(BlockError) as e:
        _post_multi_order(client, content, {'down': t4.pk})
    assert 'Cannot move the last item down' in str(e.value)
    assert [
        t1.pk, t2.pk, t3.pk, t4.pk
    ] == [item.pk for item in content.ordered_references()]


@pytest.mark.django_db
def test_order_multi_down_invalid(client):
    content = TitleFactory()
    t1, t2, t3, t4 = _set_up_order_multi(content)
    with pytest.raises(BlockError) as e:
        _post_multi_order(client, content, {'down': t1.pk+t2.pk+t3.pk+t4.pk})
    assert 'Cannot find item' in str(e.value)
    assert [
        t1.pk, t2.pk, t3.pk, t4.pk
    ] == [item.pk for item in content.ordered_references()]


@pytest.mark.django_db
def test_order_multi_up_1(client):
    """Trying to move the first item up, should raise an exception."""
    content = TitleFactory()
    t1, t2, t3, t4 = _set_up_order_multi(content)
    with pytest.raises(BlockError) as e:
        _post_multi_order(client, content, {'up': t1.pk})
    assert 'Cannot move the first item up' in str(e.value)
    assert [
        t1.pk, t2.pk, t3.pk, t4.pk
    ] == [item.pk for item in content.ordered_references()]


@pytest.mark.django_db
def test_order_multi_up_2(client):
    content = TitleFactory()
    t1, t2, t3, t4 = _set_up_order_multi(content)
    _post_multi_order(client, content, {'up': t2.pk})
    assert [
        t2.pk, t1.pk, t3.pk, t4.pk
    ] == [item.pk for item in content.ordered_references()]


@pytest.mark.django_db
def test_order_multi_up_4(client):
    content = TitleFactory()
    t1, t2, t3, t4 = _set_up_order_multi(content)
    _post_multi_order(client, content, {'up': t4.pk})
    assert [
        t1.pk, t2.pk, t4.pk, t3.pk
    ] == [item.pk for item in content.ordered_references()]


@pytest.mark.django_db
def test_order_multi_up_invalid(client):
    content = TitleFactory()
    t1, t2, t3, t4 = _set_up_order_multi(content)
    with pytest.raises(BlockError) as e:
        _post_multi_order(client, content, {'up': t1.pk+t2.pk+t3.pk+t4.pk})
    assert 'Cannot find item' in str(e.value)
    assert [
        t1.pk, t2.pk, t3.pk, t4.pk
    ] == [item.pk for item in content.ordered_references()]


@pytest.mark.django_db
def test_select_multi(client):
    link_1 = LinkFactory()
    link_2 = LinkFactory()
    link_3 = LinkFactory()
    link_4 = LinkFactory()
    content = TitleFactory()
    through_1 = TitleLinkFactory(content=content, link=link_1, order=4)
    TitleLinkFactory(content=content, link=link_2, order=3)
    through_3 = TitleLinkFactory(content=content, link=link_3, order=2)
    TitleLinkFactory(content=content, link=link_4, order=1)
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = url_link_multi(content, 'block.wizard.link.select')
    data = {
        'many_to_many': [through_1.pk, through_3.pk],
    }
    response = client.post(url, data)
    # check
    assert 302 == response.status_code
    expect = url_link_multi(content, 'block.wizard.link.option')
    assert expect in response['Location']
    content.refresh_from_db()
    assert 2 == content.references.count()
    qs = content.ordered_references()
    result = [item.link.pk for item in qs]
    assert link_1.pk in result and link_3.pk in result
    # ordering controlled by 'ordering' on 'TitleLink' model
    assert [1, 2] == [item.order for item in qs]

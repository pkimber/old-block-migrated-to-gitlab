# -*- encoding: utf-8 -*-
import io
import PIL
import pytest

from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse

from block.models import (
    Image,
    Wizard,
)
from block.tests.factories import (
    ImageCategoryFactory,
    ImageFactory,
)
from example_block.tests.factories import (
    TitleFactory,
    TitleImageFactory,
)
from login.tests.factories import (
    TEST_PASSWORD,
    UserFactory,
)


def _reverse_url(content, url_name, field_name, wizard_type, category):
    """Get the wizard url for a piece of content."""
    content_type = ContentType.objects.get_for_model(content)
    kwargs = {
        'content': content_type.pk,
        'pk': content.pk,
        'field': field_name,
        'type': wizard_type,
    }
    if category:
        kwargs.update(category=category.slug)
    return reverse(url_name, kwargs=kwargs)


def url_multi(content, url_name, category=None):
    return _reverse_url(content, url_name, 'slideshow', Wizard.MULTI, category)


def url_single(content, url_name, category=None):
    return _reverse_url(content, url_name, 'picture', Wizard.SINGLE, category)


@pytest.mark.django_db
def test_wizard_image_choose_multi(client):
    content = TitleFactory()
    ImageFactory()
    image_1 = ImageFactory()
    image_2 = ImageFactory()
    user = UserFactory(is_staff=True)
    assert content.picture is None
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = url_multi(content, 'block.wizard.image.choose')
    data = {
        'images': [image_2.pk, image_1.pk],
    }
    response = client.post(url, data)
    # check
    assert 302 == response.status_code
    expect = url_multi(content, 'block.wizard.image.option')
    assert expect in response['Location']
    content.refresh_from_db()
    assert 2 == content.slideshow.count()
    # ordering controlled by 'ordering' on 'TitleImage' model
    qs = content.slideshow.through.objects.all()
    assert [1, 2] == [item.order for item in qs]


@pytest.mark.django_db
def test_wizard_image_choose_single(client):
    content = TitleFactory()
    ImageFactory()
    image = ImageFactory()
    user = UserFactory(is_staff=True)
    assert content.picture is None
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = url_single(content, 'block.wizard.image.choose')
    data = {
        'images': image.pk,
    }
    response = client.post(url, data)
    # check
    assert 302 == response.status_code
    expect = content.block.page_section.page.get_design_url()
    assert expect in response['Location']
    content.refresh_from_db()
    assert image == content.picture


@pytest.mark.django_db
def test_wizard_image_choose_category_multi(client):
    """Choose from images in the selected category."""
    content = TitleFactory()
    category = ImageCategoryFactory()
    image_1 = ImageFactory()
    image_2 = ImageFactory(category=category)
    image_3 = ImageFactory(category=category)
    image_4 = ImageFactory(category=category)
    user = UserFactory(is_staff=True)
    assert content.picture is None
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = url_multi(content, 'block.wizard.image.choose', category=category)
    assert category.slug in url
    data = {
        'images': [image_2.pk, image_4.pk],
    }
    response = client.post(url, data)
    # check
    assert 302 == response.status_code
    expect = url_multi(content, 'block.wizard.image.option')
    assert expect in response['Location']
    content.refresh_from_db()
    assert 2 == content.slideshow.count()
    # ordering controlled by 'ordering' on 'TitleImage' model
    qs = content.slideshow.through.objects.all()
    assert [1, 2] == [item.order for item in qs]


@pytest.mark.django_db
def test_wizard_image_choose_category_single(client):
    """Choose from images in the selected category."""
    content = TitleFactory()
    category = ImageCategoryFactory()
    ImageFactory()
    image = ImageFactory(category=category)
    user = UserFactory(is_staff=True)
    assert content.picture is None
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = url_single(content, 'block.wizard.image.choose', category=category)
    assert category.slug in url
    data = {
        'images': image.pk,
    }
    response = client.post(url, data)
    # check
    assert 302 == response.status_code
    expect = content.block.page_section.page.get_design_url()
    assert expect in response['Location']
    content.refresh_from_db()
    assert image == content.picture


@pytest.mark.django_db
def test_wizard_image_remove_single(client):
    """The multi test for removing is ``test_wizard_image_select_multi``."""
    image = ImageFactory()
    content = TitleFactory(picture=image)
    user = UserFactory(is_staff=True)
    assert content.picture is not None
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = url_single(content, 'block.wizard.image.remove')
    response = client.post(url)
    # check
    content.refresh_from_db()
    expect = content.block.page_section.page.get_design_url()
    assert 302 == response.status_code
    assert expect in response['Location']
    assert content.picture is None


@pytest.mark.django_db
def test_wizard_image_select_multi(client):
    """The single test for removing is ``test_wizard_image_remove_single``."""
    image_1 = ImageFactory()
    image_2 = ImageFactory()
    image_3 = ImageFactory()
    image_4 = ImageFactory()
    content = TitleFactory()
    through_1 = TitleImageFactory(content=content, image=image_1, order=4)
    through_2 = TitleImageFactory(content=content, image=image_2, order=3)
    through_3 = TitleImageFactory(content=content, image=image_3, order=2)
    through_4 = TitleImageFactory(content=content, image=image_4, order=1)
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = url_multi(content, 'block.wizard.image.select')
    data = {
        'many_to_many': [through_1.pk, through_3.pk],
    }
    response = client.post(url, data)
    # check
    assert 302 == response.status_code
    expect = url_multi(content, 'block.wizard.image.option')
    assert expect in response['Location']
    content.refresh_from_db()
    assert 2 == content.slideshow.count()
    qs = content.slideshow.through.objects.all()
    result = [item.image.pk for item in qs]
    assert image_1.pk in result and image_3.pk in result
    # ordering controlled by 'ordering' on 'TitleImage' model
    assert [1, 2] == [item.order for item in qs]


@pytest.mark.django_db
def test_wizard_image_upload_multi(client):
    content = TitleFactory()
    category = ImageCategoryFactory()
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = url_multi(content, 'block.wizard.image.upload')
    # create an image ready to upload
    fp = io.BytesIO()
    PIL.Image.new('1', (1,1)).save(fp, 'png')
    fp.seek(0)
    image_file = SimpleUploadedFile(
        'file.png',
        fp.read(),
        content_type='image/png'
    )
    data = {
        'add_to_library': True,
        'category': category.pk,
        'image': image_file,
        'title': 'Cricket',
    }
    response = client.post(url, data)
    # check
    content.refresh_from_db()
    assert 302 == response.status_code
    expect = url_multi(content, 'block.wizard.image.option')
    assert expect in response['Location']
    assert 1 == content.slideshow.count()
    image = content.slideshow.first()
    assert 'Cricket' == image.title
    assert image.category == category
    assert image.deleted is False
    # check an image has been added to the database
    assert 1 == Image.objects.count()


@pytest.mark.django_db
def test_wizard_image_upload_single(client):
    content = TitleFactory()
    category = ImageCategoryFactory()
    ImageFactory()
    #image = ImageFactory()
    user = UserFactory(is_staff=True)
    assert content.picture is None
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = url_single(content, 'block.wizard.image.upload')
    # create an image ready to upload
    fp = io.BytesIO()
    PIL.Image.new('1', (1,1)).save(fp, 'png')
    fp.seek(0)
    image_file = SimpleUploadedFile(
        'file.png',
        fp.read(),
        content_type='image/png'
    )
    data = {
        'add_to_library': True,
        'category': category.pk,
        'image': image_file,
        'title': 'Cricket',
    }
    response = client.post(url, data)
    # check
    content.refresh_from_db()
    expect = content.block.page_section.page.get_design_url()
    assert 302 == response.status_code
    assert expect in response['Location']
    assert 'Cricket' == content.picture.title
    assert content.picture is not None
    assert content.picture.category == category
    assert content.picture.deleted is False
    # check an image has been added to the database
    assert 2 == Image.objects.count()

# -*- encoding: utf-8 -*-
import io
import pytest

from PIL import Image

from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse

from block.models import Wizard
from block.tests.factories import (
    ImageCategoryFactory,
    ImageFactory,
)
from example_block.tests.factories import TitleFactory
from login.tests.factories import (
    TEST_PASSWORD,
    UserFactory,
)


def reverse_url(content, url_name):
    """Get the wizard url for a piece of content."""
    content_type = ContentType.objects.get_for_model(content)
    return reverse(
        url_name,
        kwargs={
            'content': content_type.pk,
            'pk': content.pk,
            'field': 'picture',
            'type': Wizard.SINGLE,
        }
    )


@pytest.mark.django_db
def test_wizard_image_choose(client):
    content = TitleFactory()
    ImageFactory()
    image = ImageFactory()
    user = UserFactory(is_staff=True)
    assert content.picture is None
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = reverse_url(content, 'block.wizard.image.choose')
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
def test_wizard_image_remove(client):
    image = ImageFactory()
    content = TitleFactory(picture=image)
    user = UserFactory(is_staff=True)
    assert content.picture is not None
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = reverse_url(content, 'block.wizard.image.remove')
    response = client.post(url)
    # check
    content.refresh_from_db()
    expect = content.block.page_section.page.get_design_url()
    assert 302 == response.status_code
    assert expect in response['Location']
    assert content.picture is None


@pytest.mark.django_db
def test_wizard_image_upload(client):
    content = TitleFactory()
    category = ImageCategoryFactory()
    ImageFactory()
    #image = ImageFactory()
    user = UserFactory(is_staff=True)
    assert content.picture is None
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    url = reverse_url(content, 'block.wizard.image.upload')
    # create an image ready to upload
    fp = io.BytesIO()
    Image.new('1', (1,1)).save(fp, 'png')
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

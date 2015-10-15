# -*- encoding: utf-8 -*-
import io
import pytest

from PIL import Image

from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from block.forms import (
    ImageForm,
    ImageListForm,
    ImageTypeForm,
)
from block.tests.factories import ImageFactory
from example_block.tests.factories import TitleFactory
from login.tests.factories import (
    TEST_PASSWORD,
    UserFactory,
)
from login.tests.fixture import perm_check



def picture_url(content):
    """Get the picture URL from the wizard URLs for the content object."""
    wizard_urls = content.wizard_urls
    return next(x['url'] for x in wizard_urls if 'Picture' in x['caption'])


@pytest.mark.django_db
def test_perm(perm_check):
    content = TitleFactory()
    url = picture_url(content)
    perm_check.staff(url)


@pytest.mark.django_db
def test_page_initial(client):
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    content = TitleFactory()
    url = picture_url(content)
    response = client.get(url)
    assert 200 == response.status_code
    form = response.context['form']
    assert ImageTypeForm == form.__class__


@pytest.mark.django_db
def test_page_initial_to_image_form(client):
    """Choose to upload an image."""
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    content = TitleFactory()
    url = picture_url(content)
    data = {
        'image_wizard-current_step': ImageTypeForm.FORM_IMAGE_TYPE,
        'image_type-image_type': ImageTypeForm.FORM_IMAGE,
    }
    response = client.post(url, data)
    assert 200 == response.status_code
    form = response.context['form']
    assert ImageForm == form.__class__


@pytest.mark.django_db
def test_page_initial_to_image_list(client):
    """Choose from a list of images."""
    ImageFactory()
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    content = TitleFactory()
    url = picture_url(content)
    data = {
        'image_wizard-current_step': ImageTypeForm.FORM_IMAGE_TYPE,
        'image_type-image_type': ImageTypeForm.FORM_IMAGE_LIST,
    }
    response = client.post(url, data)
    assert 200 == response.status_code
    form = response.context['form']
    assert ImageListForm == form.__class__


@pytest.mark.django_db
def test_image_list_to_done(client):
    """Choose an image from the list."""
    ImageFactory()
    image = ImageFactory()
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    session = client.session
    # https://www.pkimber.net/howto/django/testing/wizard.html
    session['wizard_image_wizard'] = {
        'step_data': {
            'image_type': {
                'image_type-image_type': [ImageTypeForm.FORM_IMAGE_LIST],
            }
        },
        'step': ImageTypeForm.FORM_IMAGE_LIST,
        'extra_data': {},
        'step_files': {ImageTypeForm.FORM_IMAGE_TYPE: {}}
    }
    session.save()
    content = TitleFactory()
    url = picture_url(content)
    data = {
        'image_wizard-current_step': ImageTypeForm.FORM_IMAGE_LIST,
        'a-images': image.pk,
    }
    response = client.post(url, data)
    assert 302 == response.status_code
    # make sure we redirect to page design
    page_design_url = content.block.page_section.page.get_design_url()
    assert page_design_url in response['Location']
    # check image is attached
    content.refresh_from_db()
    assert image.pk == content.picture.pk


@pytest.mark.django_db
def test_image_remove_to_done(client):
    """Remove an image from the page."""
    #ImageFactory()
    #image = ImageFactory()
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    session = client.session
    # https://www.pkimber.net/howto/django/testing/wizard.html
    session['wizard_image_wizard'] = {
        'extra_data': {},
        'step_data': {
            'image_type': {
                'image_type-image_type': [ImageTypeForm.REMOVE],
            }
        },
        'step': ImageTypeForm.FORM_IMAGE_TYPE,
        'step_files': {ImageTypeForm.FORM_IMAGE_TYPE: {}}
    }
    session.save()
    content = TitleFactory(picture=ImageFactory())
    url = picture_url(content)
    data = {
        'image_wizard-current_step': ImageTypeForm.FORM_IMAGE_TYPE,
        'image_type-image_type': ImageTypeForm.REMOVE,
    }
    response = client.post(url, data)
    assert 302 == response.status_code
    # make sure we redirect to page design
    page_design_url = content.block.page_section.page.get_design_url()
    assert page_design_url in response['Location']
    # check image is removed
    content.refresh_from_db()
    assert content.picture is None


@pytest.mark.django_db
def test_image_upload_to_done(client):
    """Upload an image and attach to the content."""
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    session = client.session
    # https://www.pkimber.net/howto/django/testing/wizard.html
    session['wizard_image_wizard'] = {
        'extra_data': {},
        'step_data': {
            'image_type': {
                'image_type-image_type': [ImageTypeForm.FORM_IMAGE],
            },
        },
        'step': ImageTypeForm.FORM_IMAGE,
        'step_files': {ImageTypeForm.FORM_IMAGE_TYPE: {}},
    }
    session.save()
    content = TitleFactory(picture=ImageFactory())
    # create an image ready to upload
    url = picture_url(content)
    fp = io.BytesIO()
    Image.new('1', (1,1)).save(fp, 'png')
    fp.seek(0)
    image = SimpleUploadedFile("file.png", fp.read(), content_type="image/png")
    data = {
        'image_wizard-current_step': ImageTypeForm.FORM_IMAGE,
        'image_type-image_type': ImageTypeForm.REMOVE,
        'i-title': 'My Image Title',
        'i-image': image,
    }
    response = client.post(url, data)
    assert 302 == response.status_code
    # make sure we redirect to page design
    page_design_url = content.block.page_section.page.get_design_url()
    assert page_design_url in response['Location']
    # check image has been uploaded and attached
    content.refresh_from_db()
    assert content.picture is not None
    assert 'My Image Title' == content.picture.title


@pytest.mark.django_db
def test_image_delete_to_start(client):
    """Delete an image from the library."""
    image_1 = ImageFactory()
    image_2 = ImageFactory()
    image_3 = ImageFactory()
    user = UserFactory(is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    session = client.session
    # https://www.pkimber.net/howto/django/testing/wizard.html
    session['wizard_image_wizard'] = {
        'extra_data': {},
        'step': 'image_type',
        'step_data': {
            'image_type': {
                'image_type-image_type': [ImageTypeForm.FORM_LIST_DELETE],
            }
        },
        'step_files': {
            'list_delete': {},
            'image_type': {}
        }
    }
    session.save()
    content = TitleFactory(picture=ImageFactory())
    url = picture_url(content)

    data = {
        'image_wizard-current_step': ImageTypeForm.FORM_LIST_DELETE,
        '{}-images'.format(ImageTypeForm.FORM_LIST_DELETE): [
            image_1.pk,
            image_3.pk,
        ],
    }
    response = client.post(url, data)
    assert 200 == response.status_code
    # check image has been deleted from the library
    image_1.refresh_from_db()
    image_2.refresh_from_db()
    image_3.refresh_from_db()
    assert image_1.deleted is True
    assert image_2.deleted is False
    assert image_3.deleted is True

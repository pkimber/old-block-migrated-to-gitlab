# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

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
                'image_wizard-current_step': ['image_type'],
                'image_type-image_type': ['a'],
                'csrfmiddlewaretoken': ['WdhBpAqzd2tuT5gc9HCiKqT6tsZb']
            }
        },
        'step': ImageTypeForm.FORM_IMAGE_LIST,
        'extra_data': {},
        'step_files': {'image_type': {}}
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
                'image_wizard-current_step': [ImageTypeForm.FORM_IMAGE_TYPE],
                'csrfmiddlewaretoken': ['H1VQUMYxcPg9UTOH0lLmeYmw1SIhItIo']
            }
        },
        'step': 'image_type',
        'step_files': {'image_type': {}}
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
                'image_type-image_type': ['i'],
                'image_wizard-current_step': ['image_type'],
                'csrfmiddlewaretoken': ['H1VQUMYxcPg9UTOH0lLmeYmw1SIhItIo']
            },
            'i': {
                'i-title': ['TEst'],
                'image_wizard-current_step': ['i'],
                'csrfmiddlewaretoken': ['H1VQUMYxcPg9UTOH0lLmeYmw1SIhItIo']
            }
        },
        'step': 'i',
        'step_files': {
            'image_type': {},
            'i': {
                'i-image': {
                    'name': '80x80-place.png',
                    'charset': None,
                    'size': 260,
                    'content_type': 'image/png',
                    'tmp_name': '80x80-place.png',
                }
            }
        }
    }
    session.save()
    content = TitleFactory(picture=ImageFactory())
    url = picture_url(content)
    from django.core.files.uploadedfile import SimpleUploadedFile
    import io
    #from django.utils.image import Image
    from PIL import Image #, ImageDraw
    fp = io.BytesIO()
    Image.new('P', (1,1)).save(fp, 'png')
    fp.seek(0)

    #img = Image.new('RGBA',(100, 100))

    image = SimpleUploadedFile(
        "file.png",
        fp.read(),
        #bytes("file_content", 'UTF-8'),
        content_type="image/png",
    )
    data = {
        'image_wizard-current_step': ImageTypeForm.FORM_IMAGE,
        'image_type-image_type': ImageTypeForm.REMOVE,
        'i-title': 'Title for My Image',
        'i-image': image,
    }
    response = client.post(url, data)
    assert 302 == response.status_code
    # make sure we redirect to page design
    page_design_url = content.block.page_section.page.get_design_url()
    assert page_design_url in response['Location']
    # check image is removed
    content.refresh_from_db()
    assert content.picture is not None

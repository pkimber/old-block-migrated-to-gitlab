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
def test_page_initial_post_initial_to_image_form(client):
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
def test_page_initial_post_initial_to_image_list(client):
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
def test_page_initial_post_image_list_to(client):
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
        'step': 'a',
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
    page_design_url = content.block.page_section.page.get_design_url()
    assert page_design_url in response['Location']
    content.refresh_from_db()
    assert image.pk == content.picture.pk

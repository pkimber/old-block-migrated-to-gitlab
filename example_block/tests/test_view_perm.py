# -*- encoding: utf-8 -*-
import pytest

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from block.models import Wizard
from example_block.tests.factories import TitleFactory
from login.tests.fixture import perm_check


def reverse_url(content, url_name):
    """Get the wizard url for a piece of content."""
    content_type = ContentType.objects.get_for_model(content)
    return reverse(
        url_name,
        kwargs={
            'content': content_type.pk,
            'pk': content.pk,
            'field': 'picture',
            'type': Wizard.IMAGE,
        }
    )


@pytest.mark.django_db
def test_wizard_image_choose(perm_check):
    content = TitleFactory()
    url = reverse_url(content, 'block.wizard.image.choose')
    perm_check.staff(url)


@pytest.mark.django_db
def test_wizard_image_option(perm_check):
    content = TitleFactory()
    url = reverse_url(content, 'block.wizard.image.option')
    perm_check.staff(url)


@pytest.mark.django_db
def test_wizard_image_remove(perm_check):
    content = TitleFactory()
    url = reverse_url(content, 'block.wizard.image.remove')
    perm_check.staff(url)


@pytest.mark.django_db
def test_wizard_image_upload(perm_check):
    content = TitleFactory()
    url = reverse_url(content, 'block.wizard.image.upload')
    perm_check.staff(url)

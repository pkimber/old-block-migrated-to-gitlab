# -*- encoding: utf-8 -*-
import pytest

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from block.models import Wizard
from block.tests.factories import ImageFactory
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

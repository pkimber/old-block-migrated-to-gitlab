# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

from example_block.tests.factories import TitleFactory
from login.tests.fixture import perm_check


@pytest.mark.django_db
def test_perm(perm_check):
    urls = TitleFactory().wizard_urls
    url = next(x['url'] for x in urls if 'Link' in x['caption'])
    perm_check.staff(url)

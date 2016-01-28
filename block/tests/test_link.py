# -*- encoding: utf-8 -*-
import pytest

from block.models import Link
from block.tests.factories import UrlFactory


@pytest.mark.django_db
def test_create_external_link():
    Link.objects.create_external_link('http://www.bbc.co.uk/', 'News')


@pytest.mark.django_db
def test_create_internal_link():
    url = UrlFactory()
    Link.objects.create_internal_link(url)

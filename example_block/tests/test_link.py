# -*- encoding: utf-8 -*-
import pytest

from block.models import Link
from block.tests.factories import LinkFactory


@pytest.mark.django_db
def test_str():
    """This value is used for the select drop down in the form."""
    link = LinkFactory(title='Cricket')
    assert 'Cricket' == str(link)


@pytest.mark.django_db
def test_open_in_tab_document():
    link = LinkFactory(link_type=Link.DOCUMENT)
    assert link.open_in_tab is True


@pytest.mark.django_db
def test_open_in_tab_external():
    link = LinkFactory()
    assert link.open_in_tab is True


@pytest.mark.django_db
def test_open_in_tab_internal():
    link = LinkFactory(link_type=Link.URL_INTERNAL)
    assert link.open_in_tab is False

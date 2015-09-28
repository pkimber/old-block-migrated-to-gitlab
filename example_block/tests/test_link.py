# -*- encoding: utf-8 -*-
import pytest

from block.tests.factories import LinkFactory


@pytest.mark.django_db
def test_link_str():
    """This value is used for the select drop down in the form."""
    link = LinkFactory(title='Cricket')
    assert 'Cricket' == str(link)

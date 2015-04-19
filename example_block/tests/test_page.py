# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

from block.models import BlockError
from block.tests.scenario import (
    default_scenario_block,
    get_page_custom_calendar,
    get_page_info,
)


@pytest.mark.django_db
def test_custom_url(client):
    """Custom page, on it's own URL, so should display correctly."""
    default_scenario_block()
    page = get_page_custom_calendar()
    response = client.get(reverse('calendar.information'))
    assert 200 == response.status_code
    assert 'Jan' in str(response.content)
    assert 'Feb' in str(response.content)
    assert 'Mar' in str(response.content)


@pytest.mark.django_db
def test_custom_url_page_view(client):
    """Custom page, on it's block URL, so should throw an exception."""
    default_scenario_block()
    page = get_page_custom_calendar()
    with pytest.raises(BlockError) as excinfo:
        client.get(page.get_absolute_url())
    assert 'should not match' in str(excinfo.value)


@pytest.mark.django_db
def test_standard_url(client):
    """A standard block page should display without errors."""
    default_scenario_block()
    page = get_page_info()
    response = client.get(page.get_absolute_url())
    assert 200 == response.status_code


@pytest.mark.django_db
def test_standard_url_reverse(client):
    """A standard block page should display without errors."""
    default_scenario_block()
    url = reverse('project.page', kwargs=dict(page='info'))
    response = client.get(url)
    assert 200 == response.status_code

# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

from block.tests.factories import (
    ImageFactory,
    PageFactory,
)
from login.tests.fixture import perm_check


@pytest.mark.django_db
def test_create(perm_check):
    perm_check.staff(reverse('block.page.create'))


@pytest.mark.django_db
def test_delete(perm_check):
    page = PageFactory()
    perm_check.staff(reverse('block.page.delete', kwargs=dict(pk=page.pk)))


@pytest.mark.django_db
def test_header_footer_update(perm_check):
    perm_check.staff(reverse('block.header.footer.update'))


@pytest.mark.django_db
def test_image_delete(perm_check):
    ImageFactory()
    url = reverse('block.image.delete')
    perm_check.staff(url)


@pytest.mark.django_db
def test_list(perm_check):
    perm_check.staff(reverse('block.page.list'))


@pytest.mark.django_db
def test_update(perm_check):
    page = PageFactory()
    perm_check.staff(reverse('block.page.update', kwargs=dict(pk=page.pk)))

# -*- encoding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

from block.tests.factories import (
    ImageCategoryFactory,
    ImageFactory,
    LinkCategoryFactory,
    LinkFactory,
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
def test_image(perm_check):
    """Image library."""
    ImageFactory()
    url = reverse('block.image.list')
    perm_check.staff(url)


@pytest.mark.django_db
def test_image_delete(perm_check):
    ImageFactory()
    url = reverse('block.image.list.delete')
    perm_check.staff(url)


@pytest.mark.django_db
def test_image_update(perm_check):
    image = ImageFactory()
    url = reverse('block.image.update', args=[image.pk])
    perm_check.staff(url)


@pytest.mark.django_db
def test_list(perm_check):
    perm_check.staff(reverse('block.page.list'))


@pytest.mark.django_db
def test_update(perm_check):
    page = PageFactory()
    perm_check.staff(reverse('block.page.update', kwargs=dict(pk=page.pk)))


@pytest.mark.django_db
def test_image_category(perm_check):
    perm_check.staff(reverse('block.image.category.list'))


@pytest.mark.django_db
def test_image_category_create(perm_check):
    perm_check.staff(reverse('block.image.category.create'))


@pytest.mark.django_db
def test_image_category_delete(perm_check):
    obj = ImageCategoryFactory()
    perm_check.staff(reverse('block.image.category.delete', args=[obj.pk]))


@pytest.mark.django_db
def test_image_category_update(perm_check):
    obj = ImageCategoryFactory()
    perm_check.staff(reverse('block.image.category.update', args=[obj.pk]))


@pytest.mark.django_db
def test_link_category(perm_check):
    perm_check.staff(reverse('block.link.category.list'))


@pytest.mark.django_db
def test_link_category_create(perm_check):
    perm_check.staff(reverse('block.link.category.create'))


@pytest.mark.django_db
def test_link_category_delete(perm_check):
    obj = LinkCategoryFactory()
    perm_check.staff(reverse('block.link.category.delete', args=[obj.pk]))


@pytest.mark.django_db
def test_link_category_update(perm_check):
    obj = LinkCategoryFactory()
    perm_check.staff(reverse('block.link.category.update', args=[obj.pk]))


@pytest.mark.django_db
def test_link_document_create(perm_check):
    perm_check.staff(reverse('block.link.document.create', ))


@pytest.mark.django_db
def test_link_delete(perm_check):
    obj = LinkFactory()
    perm_check.staff(reverse('block.link.delete', args=[obj.pk]))


@pytest.mark.django_db
def test_link_document_update(perm_check):
    obj = LinkFactory()
    perm_check.staff(reverse('block.link.document.update', args=[obj.pk]))


@pytest.mark.django_db
def test_link_external_update(perm_check):
    obj = LinkFactory()
    perm_check.staff(reverse('block.link.external.update', args=[obj.pk]))


@pytest.mark.django_db
def test_link_internal_update(perm_check):
    obj = LinkFactory()
    perm_check.staff(reverse('block.link.internal.update', args=[obj.pk]))

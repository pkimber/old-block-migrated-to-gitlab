# -*- encoding: utf-8 -*-
import pytest
from django.core.urlresolvers import reverse
from django.test import TestCase

from block.models import Page
from block.tests.factories import TemplateFactory
from login.tests.factories import (
    TEST_PASSWORD,
    UserFactory,
)
from .factories import (
    PageFactory,
    SectionFactory,
    TemplateFactory,
    TemplateSectionFactory,
)


@pytest.mark.django_db
def test_add_section_to_template(client):
    """'setup_page' will update all the pages with the new sections."""
    template = TemplateFactory()
    section_a = SectionFactory(slug='section_a', name='Section A')
    user = UserFactory(is_superuser=True, is_staff=True)
    page_1 = PageFactory(order=1, template=template)
    page_2 = PageFactory(order=2)
    page_3 = PageFactory(order=3, template=template)
    assert 0 == page_1.pagesection_set.all().count()
    assert 0 == page_2.pagesection_set.all().count()
    assert 0 == page_3.pagesection_set.all().count()

    assert client.login(username=user.username, password=TEST_PASSWORD)
    response = client.post(
        reverse('block.template.section.create', args = [template.pk]),
        dict(
            section=section_a.pk,
        ))
    assert 302 == response.status_code
    expect = "http://testserver" + reverse('block.template.list')
    assert expect == response["Location"]
    assert 1 == page_1.pagesection_set.all().count()
    assert 0 == page_2.pagesection_set.all().count()
    assert 1 == page_3.pagesection_set.all().count()

@pytest.mark.django_db
def test_remove_section_from_template(client):
    """'setup_page' will update all the pages with the new sections."""
    template_a = TemplateFactory()
    TemplateSectionFactory(template=template_a)
    section_a = SectionFactory(slug='section_a', name='Section A')
    template_section = TemplateSectionFactory(
        section=section_a, template=template_a
    )
    template_b = TemplateFactory()
    TemplateSectionFactory(template=template_b)
    TemplateSectionFactory(template=template_b)
    user = UserFactory(is_superuser=True, is_staff=True)
    page_1 = PageFactory(order=1, template=template_a)
    page_2 = PageFactory(order=2, template=template_b)
    page_3 = PageFactory(order=3, template=template_a)
    Page.objects.refresh_sections_from_template(template_a)
    Page.objects.refresh_sections_from_template(template_b)
    assert 2 == page_1.pagesection_set.all().count()
    assert 2 == page_2.pagesection_set.all().count()
    assert 2 == page_3.pagesection_set.all().count()

    assert client.login(username=user.username, password=TEST_PASSWORD)
    response = client.post(
        reverse('block.template.section.remove', args = [template_section.pk])
    )
    assert 302 == response.status_code
    # import ipdb; ipdb.set_trace()
    expect = "http://testserver" + reverse('block.template.list')
    assert expect == response["Location"]
    assert 1 == page_1.pagesection_set.all().count()
    assert 2 == page_2.pagesection_set.all().count()
    assert 1 == page_3.pagesection_set.all().count()

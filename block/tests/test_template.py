# -*- encoding: utf-8 -*-
from django.test import TestCase

from block.models import Page
from block.tests.factories import (
    PageFactory,
    PageSectionFactory,
    SectionFactory,
    TemplateFactory,
    TemplateSectionFactory,
)


class TestTemplate(TestCase):

    def test_update_page(self):
        """'setup_page' will update a page with the new sections."""
        template = TemplateFactory()
        TemplateSectionFactory(template=template)
        page = PageFactory(template=template)
        self.assertEqual(0, page.pagesection_set.all().count())
        self.assertEqual(1, template.templatesection_set.all().count())
        page.refresh_sections_from_template()
        self.assertEqual(1, page.pagesection_set.all().count())

    def test_update_pages(self):
        """'setup_page' will update all the pages with the new sections."""
        template = TemplateFactory()
        TemplateSectionFactory(template=template)
        page_1 = PageFactory(order=1, template=template)
        page_2 = PageFactory(order=2)
        page_3 = PageFactory(order=3, template=template)
        self.assertEqual(0, page_1.pagesection_set.all().count())
        self.assertEqual(0, page_2.pagesection_set.all().count())
        self.assertEqual(0, page_3.pagesection_set.all().count())
        Page.objects.refresh_sections_from_template(template)
        self.assertEqual(1, page_1.pagesection_set.all().count())
        self.assertEqual(0, page_2.pagesection_set.all().count())
        self.assertEqual(1, page_3.pagesection_set.all().count())

    def test_update_pages_delete(self):
        """'setup_page' will update all the pages with the new sections."""
        section_a = SectionFactory(slug='a')
        section_b = SectionFactory(slug='b')
        section_c = SectionFactory(slug='c')
        template = TemplateFactory()
        TemplateSectionFactory(template=template, section=section_b)
        page = PageFactory(template=template)
        PageSectionFactory(page=page, section=section_a)
        PageSectionFactory(page=page, section=section_c)
        self.assertEqual(
            ['a', 'c'],
            [p.section.slug for p in page.pagesection_set.all()]
        )
        page.refresh_sections_from_template()
        self.assertEqual(
            ['b',],
            [p.section.slug for p in page.pagesection_set.all()]
        )

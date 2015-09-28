# -*- encoding: utf-8 -*-
from django.test import TestCase

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
        page = PageFactory()
        template = TemplateFactory(template_name=page.template_name)
        TemplateSectionFactory(template=template)
        self.assertEqual(0, page.pagesection_set.all().count())
        self.assertEqual(1, template.templatesection_set.all().count())
        template.update_page(page)
        self.assertEqual(1, page.pagesection_set.all().count())

    def test_update_pages(self):
        """'setup_page' will update all the pages with the new sections."""
        page_1 = PageFactory(order=1)
        page_2 = PageFactory(order=2)
        page_3 = PageFactory(order=3, template_name=page_1.template_name)
        template = TemplateFactory(template_name=page_1.template_name)
        TemplateSectionFactory(template=template)
        self.assertEqual(0, page_1.pagesection_set.all().count())
        self.assertEqual(0, page_2.pagesection_set.all().count())
        self.assertEqual(0, page_3.pagesection_set.all().count())
        template.update_pages()
        self.assertEqual(1, page_1.pagesection_set.all().count())
        self.assertEqual(0, page_2.pagesection_set.all().count())
        self.assertEqual(1, page_3.pagesection_set.all().count())

    def test_update_pages_delete(self):
        """'setup_page' will update all the pages with the new sections."""
        page = PageFactory()
        section_a = SectionFactory(slug='a')
        section_b = SectionFactory(slug='b')
        section_c = SectionFactory(slug='c')
        PageSectionFactory(page=page, section=section_a)
        PageSectionFactory(page=page, section=section_c)
        self.assertEqual(
            ['a', 'c'],
            [p.section.slug for p in page.pagesection_set.all()]
        )
        template = TemplateFactory(template_name=page.template_name)
        TemplateSectionFactory(
            template=template,
            section=section_b,
        )
        template.update_pages()
        self.assertEqual(
            ['b',],
            [p.section.slug for p in page.pagesection_set.all()]
        )

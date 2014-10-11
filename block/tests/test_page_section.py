# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import IntegrityError
from django.test import TestCase

from block.tests.factories import (
    PageFactory,
    PageSectionFactory,
    SectionFactory,
)


class TestPageSection(TestCase):

    def setUp(self):
        self.home = PageFactory(name='Home')
        self.body = SectionFactory(name='Body')

    def test_make_page_section(self):
        PageSectionFactory(page=self.home, section=self.body)

    def test_page_section(self):
        home_body = PageSectionFactory(page=self.home, section=self.body)
        self.assertEqual('Home Body', str(home_body))

    def test_page_section_factory(self):
        PageSectionFactory()

    def test_page_section_duplicate(self):
        PageSectionFactory(page=self.home, section=self.body)
        with self.assertRaises(IntegrityError):
            PageSectionFactory(page=self.home, section=self.body)

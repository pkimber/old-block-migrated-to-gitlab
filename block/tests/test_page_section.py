# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import IntegrityError
from django.test import TestCase

from block.tests.model_maker import (
    make_page,
    make_page_section,
    make_section,
)


class TestPageSection(TestCase):

    def setUp(self):
        self.home = make_page('Home', 0, 'test.html')
        self.body = make_section(
            'Body',
            'example',
            'Title',
            'example.title.create'
        )

    def test_make_page_section(self):
        make_page_section(self.home, self.body)

    def test_page_section(self):
        home_body = make_page_section(self.home, self.body)
        self.assertEqual('Home Body', str(home_body))

    def test_page_section_duplicate(self):
        make_page_section(self.home, self.body)
        self.assertRaises(
            IntegrityError,
            make_page_section,
            self.home,
            self.body,
        )

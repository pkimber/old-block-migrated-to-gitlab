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
        self.body = make_section('Body')

    def test_make_page_section(self):
        make_page_section(
            self.home,
            self.body,
            'example',
            'Title',
            'example.title.create'
        )

    def test_page_section(self):
        home_body = make_page_section(
            self.home,
            self.body,
            'example',
            'Title',
            'example.title.create'
        )
        self.assertEqual('Home Body', str(home_body))

    def test_page_section_duplicate(self):
        home_body = make_page_section(
            self.home,
            self.body,
            'example',
            'Title',
            'example.title.create'
        )
        self.assertRaises(
            IntegrityError,
            make_page_section,
            self.home,
            self.body,
            'example',
            'Title',
            'example.title.create'
        )

# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from block.models import Page
from block.tests.model_maker import make_page


class TestPage(TestCase):

    def setUp(self):
        self.page = make_page('Home', 'home', 0, 'test.html')
        self.page = make_page('Information', 'info', 1, 'test.html')
        self.page = make_page('Portfolio', 'portfolio', 2, 'test.html')

    def test_menu(self):
        self.assertEqual(3, len(Page.objects.menu()))

    def test_menu_in(self):
        result = [p.slug for p in Page.objects.menu()]
        self.assertListEqual(
            ['home', 'info', 'portfolio'],
            result
        )

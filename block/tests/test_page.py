# -*- encoding: utf-8 -*-
from django.test import TestCase

from block.models import Page
from block.tests.factories import PageFactory


class TestPage(TestCase):

    def setUp(self):
        PageFactory(slug='home')
        PageFactory(slug='history', deleted=True)
        PageFactory(slug='info')
        PageFactory(slug='portfolio')

    def test_menu(self):
        self.assertEqual(3, len(Page.objects.menu()))

    def test_menu_in(self):
        result = [p.slug for p in Page.objects.menu()]
        self.assertListEqual(
            ['home', 'info', 'portfolio'],
            result
        )

    def test_pages(self):
        result = [p.slug for p in Page.objects.pages()]
        self.assertListEqual(
            ['home', 'info', 'portfolio'],
            result
        )

# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from block.models import Page
from block.service import init_page


class TestService(TestCase):

    def setUp(self):
        self.SLUG = 'home'
        self.HOME = 'Home'

    def test_init_not(self):
        try:
            Page.objects.get(slug=self.SLUG)
            self.fail("'{}' page exists, but hasn't been "
                "created yet".format(self.SLUG))
        except Page.DoesNotExist:
            pass

    def test_init(self):
        init_page(self.HOME, 0)
        try:
            Page.objects.get(slug=self.SLUG)
        except Page.DoesNotExist:
            self.fail("'{}' page was not initialised".format(self.SLUG))

    def test_init_change_order(self):
        # create page (order 1)
        init_page(self.HOME, 1)
        page = Page.objects.get(slug=self.SLUG)
        self.assertEqual(1, page.order)
        # update page (order 3)
        init_page(self.HOME, 3)
        page = Page.objects.get(slug=self.SLUG)
        self.assertEqual(3, page.order)

    def test_init_is_home(self):
        init_page(self.HOME, 0, is_home=True)
        page = Page.objects.get(slug=self.SLUG)
        self.assertTrue(page.is_home)

    def test_init_is_not_home(self):
        init_page(self.HOME, 0)
        page = Page.objects.get(slug=self.SLUG)
        self.assertFalse(page.is_home)

    def test_init_set_home(self):
        # create page (is not a home page)
        init_page(self.HOME, 0)
        page = Page.objects.get(slug=self.SLUG)
        self.assertFalse(page.is_home)
        # update page (is now a home page)
        init_page(self.HOME, 0, is_home=True)
        page = Page.objects.get(slug=self.SLUG)
        self.assertTrue(page.is_home)

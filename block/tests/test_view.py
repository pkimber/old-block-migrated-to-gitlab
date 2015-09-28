# -*- encoding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase

from login.tests.factories import (
    TEST_PASSWORD,
    UserFactory,
)


class TestView(TestCase):

    def setUp(self):
        self.user = UserFactory(username='staff', is_staff=True)
        self.assertTrue(
            self.client.login(
                username=self.user.username,
                password=TEST_PASSWORD
            )
        )

    def test_page_list(self):
        url = reverse('block.page.list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

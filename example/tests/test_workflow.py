# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from block.models import ModerateState
from login.tests.factories import (
    TEST_PASSWORD,
    UserFactory,
)
from example.tests.factories import TitleFactory


class TestWorkflow(TestCase):

    def setUp(self):
        user = UserFactory(username='staff', is_staff=True)
        self.assertTrue(
            self.client.login(username=user.username, password=TEST_PASSWORD)
        )
        self.block = TitleFactory().block

    def _get_pending(self):
        return self.block.content.get(
            moderate_state=ModerateState.objects._pending()
        )

    def _get_published(self):
        return self.block.content.get(
            moderate_state=ModerateState.objects._published()
        )

    def _pending_count(self):
        return self.block.content.filter(
            moderate_state=ModerateState.objects._pending()
        ).count()

    def _publish_count(self):
        return self.block.content.filter(
            moderate_state=ModerateState.objects._published()
        ).count()

    def _remove_count(self):
        return self.block.content.filter(
            moderate_state__slug=ModerateState.REMOVED
        ).count()

    def test_pending(self):
        self.assertEqual(1, self._pending_count())
        self.assertEqual(0, self._publish_count())
        self.assertEqual(0, self._remove_count())

    def test_published(self):
        self.block.publish(UserFactory())
        self.assertEqual(1, self._pending_count())
        self.assertEqual(1, self._publish_count())
        self.assertEqual(0, self._remove_count())

    def test_remove_pending(self):
        self.block.remove(UserFactory())
        self.assertEqual(0, self._pending_count())
        self.assertEqual(0, self._publish_count())
        self.assertEqual(1, self._remove_count())

    def test_remove_published(self):
        self.block.publish(UserFactory())
        self.block.remove(UserFactory())
        self.assertEqual(0, self._pending_count())
        self.assertEqual(0, self._publish_count())
        self.assertEqual(1, self._remove_count())

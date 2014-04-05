# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from block.models import (
    PENDING,
    PUBLISHED,
    REMOVED,
)
from block.tests.model_maker import (
    make_page,
    make_page_section,
    make_section,
)
from block.tests.scenario import default_block_state
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
)

from example.tests.model_maker import (
    make_title,
    make_title_block,
)


class TestWorkflow(TestCase):

    def setUp(self):
        default_block_state()
        default_scenario_login()
        home = make_page('home', 0, 'test.html')
        body = make_section('body')
        home_body = make_page_section(
            home,
            body,
            'example',
            'Title',
            'example/home.html'
        )
        self.block = make_title_block(home_body)
        self.content = make_title(
            self.block,
            1,
            'Saints'
        )

    def _get_pending(self):
        return self.block.content.get(
            moderate_state__slug=PENDING
        )

    def _get_published(self):
        return self.block.content.get(
            moderate_state__slug=PUBLISHED
        )

    def _pending_count(self):
        return self.block.content.filter(
            moderate_state__slug=PENDING
        ).count()

    def _publish_count(self):
        return self.block.content.filter(
            moderate_state__slug=PUBLISHED
        ).count()

    def _remove_count(self):
        return self.block.content.filter(
            moderate_state__slug=REMOVED
        ).count()

    def test_pending(self):
        self.assertEqual(1, self._pending_count())
        self.assertEqual(0, self._publish_count())
        self.assertEqual(0, self._remove_count())

    def test_published(self):
        self.block.publish(get_user_staff())
        self.assertEqual(1, self._pending_count())
        self.assertEqual(1, self._publish_count())
        self.assertEqual(0, self._remove_count())

    def test_remove_pending(self):
        self.block.remove(get_user_staff())
        self.assertEqual(0, self._pending_count())
        self.assertEqual(0, self._publish_count())
        self.assertEqual(1, self._remove_count())

    def test_remove_published(self):
        self.block.publish(get_user_staff())
        self.block.remove(get_user_staff())
        self.assertEqual(0, self._pending_count())
        self.assertEqual(0, self._publish_count())
        self.assertEqual(1, self._remove_count())

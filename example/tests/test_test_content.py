# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from block.models import ModerateState
from block.tests.model_maker import (
    make_container,
    make_layout,
    make_page,
    make_section,
)
from block.tests.scenario import default_moderate_state
from example.models import TestContent
from example.tests.model_maker import make_test_content


class TestTestContent(TestCase):

    def setUp(self):
        default_moderate_state()
        page = make_page('home', 0)
        body = make_layout('body')
        self.section = make_section(page, body)

    def test_next_order(self):
        #self.assertGreater(Content.objects.next_order(self.section), 3)
        pass

    def test_pending_order(self):
        """Pending items should be in 'order' order."""
        make_test_content(
            make_container(self.section, 5),
            ModerateState.pending(),
            'ABC'
        )
        make_test_content(
            make_container(self.section, 3),
            ModerateState.published(),
            'LMN'
        )
        make_test_content(
            make_container(self.section, 1),
            ModerateState.pending(),
            'XYZ'
        )
        pending = TestContent.objects.pending(self.section)
        self.assertListEqual(
            [
                'XYZ',
                'LMN',
                'ABC',
            ],
            [t.title for t in pending]
        )

    def test_published_order(self):
        """Published items should by in 'order' order."""
        make_test_content(
            make_container(self.section, 9),
            ModerateState.published(),
            'ABC'
        )
        make_test_content(
            make_container(self.section, 8),
            ModerateState.published(),
            'XYZ'
        )
        published = TestContent.objects.published(self.section)
        self.assertListEqual(
            ['XYZ', 'ABC'],
            [t.title for t in published]
        )

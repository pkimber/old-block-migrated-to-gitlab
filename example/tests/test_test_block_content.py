# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from block.models import ModerateState
from block.tests.model_maker import (
    make_container,
    make_layout,
    make_page,
)
from block.tests.scenario import default_moderate_state
from example.models import (
    TestBlock,
    TestBlockContent,
)
from example.tests.model_maker import (
    make_test_block,
    make_test_block_content,
)


class TestTestBlockContent(TestCase):

    def setUp(self):
        default_moderate_state()
        self.page = make_page('home', 0)
        self.body = make_layout('body')

    def test_next_order(self):
        #self.assertGreater(Content.objects.next_order(self.section), 3)
        pass

    def test_pending_order(self):
        """Pending items should be in 'order' order."""
        make_test_block_content(
            make_test_block(self.page, self.body),
            ModerateState.pending(),
            5,
            'ABC'
        )
        make_test_block_content(
            make_test_block(self.page, self.body),
            ModerateState.published(),
            3,
            'LMN'
        )
        make_test_block_content(
            make_test_block(self.page, self.body),
            ModerateState.pending(),
            1,
            'XYZ'
        )
        pending = TestBlockContent.objects.pending(self.page, self.body)
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
        make_test_block_content(
            make_test_block(self.page, self.body),
            ModerateState.published(),
            9,
            'ABC'
        )
        make_test_block_content(
            make_test_block(self.page, self.body),
            ModerateState.published(),
            8,
            'XYZ'
        )
        published = TestBlockContent.objects.published(self.page, self.body)
        self.assertListEqual(
            ['XYZ', 'ABC'],
            [t.title for t in published]
        )

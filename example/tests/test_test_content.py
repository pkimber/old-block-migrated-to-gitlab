# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from block.models import ModerateState
from block.tests.helper import check_content_methods
from block.tests.model_maker import (
    make_page,
    make_section,
)
from block.tests.scenario import default_moderate_state
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
)

from example.models import TestContent
from example.tests.model_maker import (
    make_test_block,
    make_test_content,
)


class TestTestContent(TestCase):

    def setUp(self):
        default_moderate_state()
        default_scenario_login()
        self.page = make_page('home', 0)
        self.body = make_section('body')

    def test_next_order(self):
        #self.assertGreater(Content.objects.next_order(self.section), 3)
        pass

    def test_content_methods(self):
        c = make_test_content(
            make_test_block(self.page, self.body),
            ModerateState.pending(),
            5,
            'ABC'
        )
        check_content_methods(c)

    def test_pending_order(self):
        """Pending items should be in 'order' order."""
        make_test_content(
            make_test_block(self.page, self.body),
            ModerateState.pending(),
            5,
            'ABC'
        )
        c = make_test_content(
            make_test_block(self.page, self.body),
            ModerateState.pending(),
            3,
            'LMN'
        )
        c.publish(get_user_staff())
        make_test_content(
            make_test_block(self.page, self.body),
            ModerateState.pending(),
            1,
            'XYZ'
        )
        pending = TestContent.objects.pending(self.page, self.body)
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
        c = make_test_content(
            make_test_block(self.page, self.body),
            ModerateState.pending(),
            9,
            'ABC'
        )
        c.publish(get_user_staff())
        c = make_test_content(
            make_test_block(self.page, self.body),
            ModerateState.pending(),
            8,
            'XYZ'
        )
        c.publish(get_user_staff())
        published = TestContent.objects.published(self.page, self.body)
        self.assertListEqual(
            ['XYZ', 'ABC'],
            [t.title for t in published]
        )

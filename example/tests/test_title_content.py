# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from block.tests.helper import check_content
from block.tests.model_maker import (
    make_page,
    make_page_section,
    make_section,
)
from block.tests.factories import PageSectionFactory
from block.tests.scenario import init_app_block
from example.tests.factories import (
    TitleBlockFactory,
    TitleFactory,
)
from login.tests.factories import UserFactory
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
)

from example.models import Title
from example.tests.model_maker import (
    make_title,
    make_title_block,
)


class TestTitle(TestCase):

    def setUp(self):
        init_app_block()
        default_scenario_login()
        home = make_page('Home', 'home', 0, 'test.html')
        body = make_section(
            'body',
            'example',
            'Title',
            'example.title.create'
        )
        self.home_body = make_page_section(home, body)

    def test_next_order(self):
        #self.assertGreater(Content.objects.next_order(self.section), 3)
        pass

    def test_content_methods(self):
        c = TitleFactory()
        check_content(c)

    def test_pending_order(self):
        """Pending items should be in 'order' order."""
        page_section = PageSectionFactory()
        # block 1
        block_1 = TitleBlockFactory(page_section=page_section)
        TitleFactory(block=block_1, title='ABC', order=5)
        # block 2 (publish)
        block_2 = TitleBlockFactory(page_section=page_section)
        TitleFactory(block=block_2, title='LMN', order=3)
        block_2.publish(UserFactory())
        # block 3 (publish)
        block_3 = TitleBlockFactory(page_section=page_section)
        TitleFactory(block=block_3, title='XYZ', order=1)
        # check order
        self.assertListEqual(
            ['XYZ', 'LMN', 'ABC'],
            [t.title for t in Title.objects.pending(page_section)]
        )

    def test_published_order(self):
        """Published items should be in 'order' order."""
        page_section = PageSectionFactory()
        # publish block 1
        block_1 = TitleBlockFactory(page_section=page_section)
        TitleFactory(block=block_1, title='ABC', order=9)
        block_1.publish(UserFactory())
        # publish block 2
        block_2 = TitleBlockFactory(page_section=page_section)
        TitleFactory(block=block_2, title='XYZ', order=8)
        block_2.publish(UserFactory())
        # check order
        self.assertListEqual(
            ['XYZ', 'ABC'],
            [t.title for t in Title.objects.published(page_section)]
        )

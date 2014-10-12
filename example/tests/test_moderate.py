# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import IntegrityError
from django.test import TestCase

from base.tests.model_maker import clean_and_save
from block.tests.scenario import get_page_section_home_body
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
)
from block.models import (
    BlockError,
    ModerateState,
)
from block.tests.factories import PageSectionFactory
from block.tests.scenario import default_scenario_block
from login.tests.factories import UserFactory
from example.models import Title
from example.tests.factories import (
    TitleBlockFactory,
    TitleFactory,
)

from example.tests.scenario import (
    default_scenario_example,
    get_block_hatherleigh_old,
    get_block_hatherleigh_three,
    get_block_hatherleigh_two,
    get_hatherleigh_old,
    get_hatherleigh_three,
    get_hatherleigh_two,
    get_jacobstowe_one_pending,
)


class TestModerate(TestCase):

    def setUp(self):
        default_scenario_login()
        default_scenario_block()
        default_scenario_example()

    def test_is_pending(self):
        block = TitleBlockFactory()
        content = TitleFactory(block=block)
        self.assertTrue(content.is_pending)

    def test_is_published(self):
        """Slightly strange test I think.  Not sure what it is doing."""
        block = TitleBlockFactory()
        content = TitleFactory(block=block)
        # publish the content
        block.publish(UserFactory())
        # get the pending content
        c = block.get_pending()
        # update the pending content
        c.title = 'Hatherleigh Three'
        c.save()
        # check the original content was published
        content = Title.objects.get(title=content.title)
        self.assertTrue(content.is_published)

    def test_is_removed(self):
        block = TitleBlockFactory()
        content = TitleFactory(block=block)
        block.remove(UserFactory())
        content = Title.objects.get(title=content.title)
        self.assertTrue(content.is_removed)

    def test_two_pending_error(self):
        block = TitleBlockFactory()
        content = TitleFactory(block=block)
        with self.assertRaises(IntegrityError):
            TitleFactory(
                block=block,
                moderate_state=ModerateState.objects._pending(),
            )

    def test_published(self):
        page_section = PageSectionFactory()
        # block_1
        block_1 = TitleBlockFactory(page_section=page_section)
        TitleFactory(block=block_1, title='content_1')
        block_1.publish(UserFactory())
        # block_2
        block_2 = TitleBlockFactory(page_section=page_section)
        TitleFactory(block=block_2, title='content_2')
        block_2.publish(UserFactory())
        # check the content is published
        result = [
            c.title for c in Title.objects.published(page_section)
        ]
        self.assertListEqual(
            [
                'content_1',
                'content_2',
            ],
            result
        )

    def test_pending(self):
        page_section = PageSectionFactory()
        # block_1
        block_1 = TitleBlockFactory(page_section=page_section)
        TitleFactory(block=block_1, title='content_1')
        # block_2
        block_2 = TitleBlockFactory(page_section=page_section)
        TitleFactory(block=block_2, title='content_2')
        # check the content is pending
        result = [
            c.title for c in Title.objects.pending(page_section)
        ]
        self.assertListEqual(
            [
                'content_1',
                'content_2',
            ],
            result
        )

    def test_publish(self):
        page_section = PageSectionFactory()
        block = TitleBlockFactory(page_section=page_section)
        TitleFactory(block=block, title='content_1')
        # check the content is pending
        self.assertListEqual(
            ['content_1',],
            [c.title for c in Title.objects.pending(page_section)],
        )
        # check the content is not published
        self.assertListEqual(
            [],
            [c.title for c in Title.objects.published(page_section)],
        )
        # publish the content
        block.publish(UserFactory())
        # check the content is not published
        self.assertListEqual(
            ['content_1',],
            [c.title for c in Title.objects.published(page_section)],
        )

    def test_remove_already(self):
        """content has already been removed and cannot be removed again."""
        block = TitleBlockFactory()
        TitleFactory(block=block)
        block.remove(UserFactory())
        with self.assertRaises(BlockError):
            block.remove(UserFactory())

    def test_remove_pending(self):
        """remove pending content."""
        page_section = PageSectionFactory()
        # block_1
        block_1 = TitleBlockFactory(page_section=page_section)
        TitleFactory(block=block_1, title='content_1')
        # block_2
        block_2 = TitleBlockFactory(page_section=page_section)
        TitleFactory(block=block_2, title='content_2')
        # check pending
        self.assertListEqual(
            ['content_1', 'content_2'],
            [c.title for c in Title.objects.pending(page_section)],
        )
        # remove block 1
        block_1.remove(UserFactory())
        # check removed
        self.assertListEqual(
            ['content_2'],
            [c.title for c in Title.objects.pending(page_section)],
        )

    def test_remove_published(self):
        """remove published content."""
        page_section = PageSectionFactory()
        # block_1
        block_1 = TitleBlockFactory(page_section=page_section)
        TitleFactory(block=block_1, title='content_1')
        block_1.publish(UserFactory())
        # block_2
        block_2 = TitleBlockFactory(page_section=page_section)
        TitleFactory(block=block_2, title='content_2')
        block_2.publish(UserFactory())
        # block_3 (not published)
        block_3 = TitleBlockFactory(page_section=page_section)
        TitleFactory(block=block_3, title='content_3')
        # check published
        self.assertListEqual(
            ['content_1', 'content_2'],
            [c.title for c in Title.objects.published(page_section)],
        )
        # remove block
        block_2.remove(UserFactory())
        # check removed
        self.assertListEqual(
            ['content_1'],
            [c.title for c in Title.objects.published(page_section)],
        )

    def test_edit_published(self):
        """edit published content."""
        page_section = PageSectionFactory()
        # block_1
        block_1 = TitleBlockFactory(page_section=page_section)
        TitleFactory(block=block_1, title='content_1')
        block_1.publish(UserFactory())
        # block_2
        block_2 = TitleBlockFactory(page_section=page_section)
        content_2 = TitleFactory(block=block_2, title='content_2')
        block_2.publish(UserFactory())
        # check pending
        self.assertListEqual(
            ['content_1', 'content_2'],
            [c.title for c in Title.objects.pending(page_section)],
        )
        # check published
        self.assertListEqual(
            ['content_1', 'content_2'],
            [c.title for c in Title.objects.published(page_section)],
        )
        # edit content
        content_2.title = 'content_2_edit'
        content_2.save()
        # check pending
        self.assertListEqual(
            ['content_1', 'content_2_edit'],
            [c.title for c in Title.objects.pending(page_section)],
        )
        # check published
        self.assertListEqual(
            ['content_1', 'content_2'],
            [c.title for c in Title.objects.published(page_section)],
        )

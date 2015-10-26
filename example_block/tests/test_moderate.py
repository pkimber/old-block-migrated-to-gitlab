# -*- encoding: utf-8 -*-
from django.db import IntegrityError
from django.test import TestCase

from block.models import (
    BlockError,
    ModerateState,
)
from block.tests.factories import (
    ImageFactory,
    PageSectionFactory,
)
from login.tests.factories import UserFactory

from example_block.models import Title
from example_block.tests.factories import (
    TitleBlockFactory,
    TitleImageFactory,
    TitleFactory,
)


class TestModerate(TestCase):

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
        TitleFactory(block=block)
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
        title = TitleFactory(
            block=block,
            title='content_1'
        )
        TitleImageFactory(content=title, image=ImageFactory(), order=1)
        TitleImageFactory(content=title, image=ImageFactory(), order=2)
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
        # check the content is published
        published = Title.objects.published(page_section)
        self.assertEqual(1, len(published))
        obj = published[0]
        self.assertEqual('content_1', obj.title)
        #self.assertListEqual(
        #    ['content_1',],
        #    [c.title for c in Title.objects.published(page_section)],
        #)

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

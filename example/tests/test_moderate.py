# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import IntegrityError
from django.test import TestCase

from base.tests.model_maker import clean_and_save
from block.tests.scenario import (
    default_moderate_state,
    get_page_home,
    get_section_body,
)
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
)
from block.models import (
    BlockError,
    ModerateState,
)
from example.models import TestContent
from example.tests.scenario import (
    default_scenario_example,
    get_block_hatherleigh_two,
    get_hatherleigh_old,
    get_hatherleigh_three,
    get_hatherleigh_two,
    get_jacobstowe_one,
)


class TestModerate(TestCase):

    def setUp(self):
        default_moderate_state()
        default_scenario_login()
        default_scenario_example()

    def test_is_pending(self):
        self.assertTrue(get_hatherleigh_three().is_pending)

    def test_is_published(self):
        self.assertTrue(get_hatherleigh_two().is_published)

    def test_is_removed(self):
        self.assertTrue(get_hatherleigh_old().is_removed)

    def test_two_pending_error(self):
        block = get_block_hatherleigh_two()
        self.assertRaises(
            IntegrityError,
            clean_and_save,
            TestContent(
                block=block,
                moderate_state=ModerateState.pending(),
                order=1,
                title='Title',
            )
        )

    def test_published(self):
        home = get_page_home()
        body = get_section_body()
        result = [
            c.title for c in TestContent.objects.published(home, body)
        ]
        self.assertListEqual(
            [
                'Hatherleigh Two',
                'Jacobstowe One',
            ],
            result
        )

    def test_pending(self):
        home = get_page_home()
        body = get_section_body()
        result = [
            c.title for c in TestContent.objects.pending(home, body)
        ]
        self.assertListEqual(
            [
                'Hatherleigh Three',
                'Jacobstowe One',
            ],
            result
        )

    def test_publish_not_pending(self):
        """This content is not 'pending' so cannot be published."""
        c = get_hatherleigh_two()
        self.assertRaises(
            BlockError,
            c.set_published,
            get_user_staff(),
        )

    def test_publish(self):
        c = get_hatherleigh_three()
        c.set_published(get_user_staff())
        c.save()
        page = get_page_home()
        section = get_section_body()
        result = list(
            TestContent.objects.published(
                page,
                section,
            ).values_list(
                'title', flat=True
            )
        )
        self.assertListEqual(
            [
                'Hatherleigh Three',
                'Jacobstowe One',
            ],
            result
        )

    def test_remove_already(self):
        """content has already been removed and cannot be removed again."""
        c = get_hatherleigh_old()
        self.assertRaises(
            BlockError,
            c.set_removed,
            get_user_staff(),
        )

    def test_remove_pending(self):
        """remove pending content."""
        content = get_hatherleigh_three()
        content.set_removed(get_user_staff())
        content.save()
        home = get_page_home()
        body = get_section_body()
        result = [
            c.title for c in TestContent.objects.pending(home, body)
        ]
        self.assertListEqual(
            [
                'Hatherleigh Two',
                'Jacobstowe One',
            ],
            result
        )

    def test_remove_published(self):
        """remove pending content."""
        content = get_hatherleigh_two()
        content.set_removed(get_user_staff())
        content.save()
        home = get_page_home()
        body = get_section_body()
        result = [
            c.title for c in TestContent.objects.published(home, body)
        ]
        self.assertListEqual(
            ['Jacobstowe One', ],
            result
        )

    def test_pending_set(self):
        """edit published content."""
        content = get_jacobstowe_one()
        content.title = 'Jacobstowe Edit'
        content.set_pending(get_user_staff())
        content.save()
        page = get_page_home()
        section = get_section_body()
        result = [
            c.title for c in TestContent.objects.pending(page, section)
        ]
        self.assertListEqual(
            [
                'Hatherleigh Three',
                'Jacobstowe Edit',
            ],
            result
        )

    def test_pending_when_pending_exists(self):
        """edit published content when content already pending.

        user should not be allowed to edit published content when pending
        content already exists in the section.

        """
        c = get_hatherleigh_two()
        self.assertRaises(
            BlockError,
            c.set_pending,
            get_user_staff()
        )

    def test_pending_when_removed(self):
        """content has been removed, so cannot set to pending."""
        c = get_hatherleigh_old()
        self.assertRaises(
            BlockError,
            c.set_pending,
            get_user_staff()
        )

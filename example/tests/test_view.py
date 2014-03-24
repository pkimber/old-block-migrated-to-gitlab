# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase

from block.models import (
    PENDING,
    PUBLISHED,
)
from block.tests.scenario import (
    default_scenario_block,
    get_page_home,
    get_section_body,
)
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
    STAFF,
)

from example.models import Title


class TestView(TestCase):

    def setUp(self):
        default_scenario_login()
        default_scenario_block()
        staff = get_user_staff()
        self.assertTrue(
            self.client.login(username=staff.username, password=STAFF)
        )

    def _create(self):
        home = get_page_home()
        body = get_section_body()
        return self.client.post(
            reverse(
                'example.title.create',
                kwargs=dict(page=home.slug, section=body.slug),
            ),
            {
                'title': 'Hatherleigh',
            },
        )

    def _get_hatherleigh(self):
        return Title.objects.get(title='Hatherleigh')

    def _get_hatherleigh_pending(self):
        return Title.objects.get(
            title='Hatherleigh',
            moderate_state__slug=PENDING,
        )

    def _get_hatherleigh_published(self):
        return Title.objects.get(
            title='Hatherleigh',
            moderate_state__slug=PUBLISHED,
        )

    def _get_hatherleigh_market(self):
        return Title.objects.get(title='Hatherleigh Market')

    def test_create(self):
        response = self._create()
        self.assertEqual(response.status_code, 302)
        title = self._get_hatherleigh()
        self.assertEqual(PENDING, title.moderate_state.slug)

    def test_update(self):
        self._create()
        title = self._get_hatherleigh()
        response = self.client.post(
            reverse(
                'example.title.update',
                kwargs=dict(pk=title.pk),
            ),
            {
                'title': 'Hatherleigh Market',
            }
        )
        self.assertEqual(response.status_code, 302)
        # Get 'Hatherleigh Market'
        self._get_hatherleigh_market()
        # 'Hatherleigh' should no longer exist
        self.assertRaises(
            Title.DoesNotExist,
            self._get_hatherleigh
        )

    def test_publish(self):
        self._create()
        title = self._get_hatherleigh()
        response = self.client.post(
            reverse(
                'example.title.publish',
                kwargs=dict(pk=title.pk),
            )
        )
        self.assertEqual(response.status_code, 302)
        self._get_hatherleigh_pending()
        self._get_hatherleigh_published()

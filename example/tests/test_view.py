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

    def _update(self):
        title = self._get_hatherleigh_pending()
        return self.client.post(
            reverse(
                'example.title.update',
                kwargs=dict(pk=title.pk),
            ),
            {
                'title': 'Hatherleigh Market',
            }
        )

    def _publish(self):
        title = self._get_hatherleigh()
        return self.client.post(
            reverse(
                'example.title.publish',
                kwargs=dict(pk=title.pk),
            )
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
        self.assertTrue(title.is_pending_added)

    def test_update(self):
        response = self._create()
        self.assertEqual(response.status_code, 302)
        response = self._update()
        self.assertEqual(response.status_code, 302)
        # Get 'Hatherleigh Market'
        title = self._get_hatherleigh_market()
        # Is not published, so should be 'pending' not 'pushed'
        self.assertTrue(title.is_pending_added)
        # 'Hatherleigh' should no longer exist
        self.assertRaises(
            Title.DoesNotExist,
            self._get_hatherleigh
        )

    def test_page_list(self):
        url = reverse('block.page.list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_publish(self):
        self._create()
        response = self._publish()
        self.assertEqual(response.status_code, 302)
        title = self._get_hatherleigh_pending()
        # Is published, so should be 'pending' and 'pushed'
        self.assertTrue(title.is_pending_pushed)
        self._get_hatherleigh_published()

    def test_publish_update(self):
        # create
        response = self._create()
        self.assertEqual(response.status_code, 302)
        # publish
        response = self._publish()
        self.assertEqual(response.status_code, 302)
        # Is published, so should be 'pending' and 'pushed'
        title = self._get_hatherleigh_pending()
        self.assertTrue(title.is_pending_pushed)
        # update
        response = self._update()
        self.assertEqual(response.status_code, 302)
        # Has been edited, so should be 'pending' not 'pushed'
        title = self._get_hatherleigh_market()
        self.assertTrue(
            title.is_pending_edited,
            'state is {} {}'.format(
                title.moderate_state.slug,
                title.edit_state.slug,
            )
        )

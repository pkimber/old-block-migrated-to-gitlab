# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase

from block.models import (
    PENDING,
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
            {'title': 'Hatherleigh'},
        )

    def test_create(self):
        response = self._create()
        self.assertEqual(response.status_code, 302)
        title = Title.objects.get(title='Hatherleigh')
        self.assertEqual(PENDING, title.moderate_state.slug)


    #def test_publish(self):
    #    c = get_title_content()
    #    response = self.client.post(
    #        reverse('example.title.publish', kwargs={'pk': c.pk}),
    #    )
    #    self.assertEqual(response.status_code, 302)

    #def test_update(self):
    #    c = get_title_content()
    #    response = self.client.post(
    #        reverse('example.title.update', kwargs={'pk': c.pk}),
    #        {'title': 'Hatherleigh'}
    #    )
    #    self.assertEqual(response.status_code, 302)

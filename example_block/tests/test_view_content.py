# -*- encoding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase

from block.models import ModerateState
from block.tests.factories import (
    PageFactory,
    PageSectionFactory,
)
from login.tests.factories import (
    TEST_PASSWORD,
    UserFactory,
)

from example_block.models import Title


class TestView(TestCase):

    def setUp(self):
        """login, so we can create, update and publish."""
        user = UserFactory(username='staff', is_staff=True)
        self.assertTrue(
            self.client.login(username=user.username, password=TEST_PASSWORD)
        )

    def _create(self, title_text):
        page = PageFactory(slug_menu='')
        page_section = PageSectionFactory(page=page)
        return self.client.post(
            reverse(
                'example.title.create',
                kwargs=dict(
                    page=page_section.page.slug,
                    section=page_section.section.slug
                ),
            ),
            {'title': title_text},
        )

    def _update(self, title, title_text):
        return self.client.post(
            reverse('example.title.update', kwargs=dict(pk=title.pk)),
            {'title': title_text}
        )

    def _publish(self, title):
        return self.client.post(
            reverse(
                'example.title.publish',
                kwargs=dict(pk=title.pk),
            )
        )

    def test_create(self):
        response = self._create('title_1')
        self.assertEqual(response.status_code, 302)
        title = Title.objects.get(title='title_1')
        self.assertEqual(ModerateState.PENDING, title.moderate_state.slug)
        self.assertTrue(title.is_pending_added)

    def test_update(self):
        """Create some content, and then update it."""
        response = self._create('title_1')
        self.assertEqual(response.status_code, 302)
        title = Title.objects.get(title='title_1')
        self.assertTrue(title.is_pending_added)
        # update the title
        response = self._update(title, 'title_2')
        self.assertEqual(response.status_code, 302)
        title = Title.objects.get(title='title_2')
        # Is not published, so should be 'pending' not 'pushed'
        self.assertTrue(title.is_pending_added)
        # 'title_1' should no longer exist
        with self.assertRaises(Title.DoesNotExist):
            Title.objects.get(title='title_1')

    def test_publish(self):
        """Create some content, and publish it."""
        self._create('title_1')
        title = Title.objects.get(title='title_1')
        response = self._publish(title)
        self.assertEqual(response.status_code, 302)
        # find the pending content
        title = Title.objects.get(
            title='title_1',
            moderate_state=ModerateState.objects._pending(),
        )
        # published, so should be 'pending' and 'pushed'
        self.assertTrue(title.is_pending_pushed)
        # find the published content
        title = Title.objects.get(
            title='title_1',
            moderate_state=ModerateState.objects._published(),
        )

    def test_publish_update(self):
        # create
        response = self._create('title_1')
        self.assertEqual(response.status_code, 302)
        # publish
        title = Title.objects.get(title='title_1')
        response = self._publish(title)
        self.assertEqual(response.status_code, 302)
        # Is published, so should be 'pending' and 'pushed'
        title = Title.objects.get(
            title='title_1',
            moderate_state=ModerateState.objects._pending(),
        )
        self.assertTrue(title.is_pending_pushed)
        # update
        response = self._update(title, 'title_2')
        self.assertEqual(response.status_code, 302)
        # Has been edited, so should be 'pending' not 'pushed'
        title = Title.objects.get(
            title='title_2',
            moderate_state=ModerateState.objects._pending(),
        )
        self.assertTrue(
            title.is_pending_edited,
            'state is {} {}'.format(
                title.moderate_state.slug,
                title.edit_state.slug,
            )
        )

# -*- encoding: utf-8 -*-
from django.core.urlresolvers import reverse

from base.tests.test_utils import PermTestCase

from block.tests.factories import PageFactory
from login.tests.factories import UserFactory


class TestViewPerm(PermTestCase):

    def setUp(self):
        UserFactory(username='staff', is_staff=True, is_superuser=True)
        UserFactory(username='web')

    def test_create(self):
        self.assert_staff_only(reverse('block.page.create'))

    def test_delete(self):
        page = PageFactory()
        self.assert_staff_only(
            reverse('block.page.delete', kwargs=dict(pk=page.pk))
        )

    def test_header_footer_update(self):
        self.assert_staff_only(reverse('block.header.footer.update'))

    def test_list(self):
        self.assert_staff_only(reverse('block.page.list'))

    def test_update(self):
        page = PageFactory()
        self.assert_staff_only(
            reverse('block.page.update', kwargs=dict(pk=page.pk))
        )

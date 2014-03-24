# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from block.management.commands import demo_data_block
from login.management.commands import demo_data_login

from example.management.commands import demo_data_example


class TestCommand(TestCase):

    def test_demo_data(self):
        """ Test the management command """
        pre = demo_data_login.Command()
        pre.handle()
        pre = demo_data_block.Command()
        pre.handle()
        command = demo_data_example.Command()
        command.handle()

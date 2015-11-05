# -*- encoding: utf-8 -*-
from django.test import TestCase

from block.tests.factories import PageFactory
from block.management.commands import (
    demo_data_block,
    init_app_block,
)


class TestCommand(TestCase):

    def test_demo_data(self):
        """ Test the management command """
        command = demo_data_block.Command()
        command.handle()

    def test_init_app(self):
        """ Test the management command """
        PageFactory()
        command = init_app_block.Command()
        command.handle()

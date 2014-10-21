# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from block.tests.scenario import init_app_block


class Command(BaseCommand):

    help = "Initialise block application"

    def handle(self, *args, **options):
        init_app_block()
        print("Initialised 'block' app...")

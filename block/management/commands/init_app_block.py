# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from block.tests.scenario import default_moderate_state


class Command(BaseCommand):

    help = "Initialise block application"

    def handle(self, *args, **options):
        default_moderate_state()
        print("Initialised 'block' app...")

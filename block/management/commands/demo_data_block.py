# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from block.tests.scenario import default_scenario_block


class Command(BaseCommand):

    help = "Create demo data for 'block'"

    def handle(self, *args, **options):
        default_scenario_block()
        print("Created 'block' demo data...")

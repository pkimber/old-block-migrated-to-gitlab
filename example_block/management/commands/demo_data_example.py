# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand

from example_block.tests.scenario import default_scenario_example


class Command(BaseCommand):

    help = "Create demo data for 'example'"

    def handle(self, *args, **options):
        default_scenario_example()
        print("Created 'example' demo data...")

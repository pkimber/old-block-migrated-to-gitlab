# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from block.models import Page
from block.tests.model_maker import make_page


class Command(BaseCommand):

    help = "Create demo data for 'block'"

    def handle(self, *args, **options):
        try:
            Page.objects.get(slug='home')
        except Page.DoesNotExist:
            make_page('Home', 0)
        try:
            Page.objects.get(slug='information')
        except Page.DoesNotExist:
            make_page('Information', 1)
        try:
            Page.objects.get(slug='portfolio')
        except Page.DoesNotExist:
            make_page('Portfolio', 2)
        print("Created 'block' demo data...")

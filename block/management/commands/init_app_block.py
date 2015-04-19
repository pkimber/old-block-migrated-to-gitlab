# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Initialise block application"

    def handle(self, *args, **options):
        print("Initialised 'block' app...")

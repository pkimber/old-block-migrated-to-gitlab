# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand

from block.models import Url


class Command(BaseCommand):

    help = "Initialise block application"

    def handle(self, *args, **options):
        Url.objects.init_pages()
        print("Initialised 'block' app...")

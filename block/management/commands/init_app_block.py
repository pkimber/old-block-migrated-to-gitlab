# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand

from block.models import (
    Page,
    Template,
    TemplateSection,
    Url,
)


class Command(BaseCommand):

    help = "Initialise block application"

    def handle(self, *args, **options):
        # add existing templates and sections
        for page in Page.objects.pages():
            template = Template.objects.init_template(page.template_name)
            for page_section in page.pagesection_set.all():
                TemplateSection.objects.init_template_section(
                    template,
                    page_section.section,
                )
            if not page.is_custom:
                Url.objects.init_page_url(page)
        print("Initialised 'block' app...")

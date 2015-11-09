# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def init_page_section(page, template, template_section_model):
    """Add the sections to the template."""
    for page_section in page.pagesection_set.all():
        try:
            template_section_model.objects.get(
                template=template,
                section=page_section.section,
            )
        except template_section_model.DoesNotExist:
            instance = template_section_model(**dict(
                template=template,
                section=page_section.section,
            ))
            instance.save()
            instance.full_clean()


def init_template(page, template_model, template_section_model):
    try:
        template = template_model.objects.get(template_name=page.template_name)
    except template_model.DoesNotExist:
        template = template_model(**dict(
            name='Our Template',
            template_name=page.template_name,
        ))
        template.save()
        template.full_clean()
    init_page_section(page, template, template_section_model)
    return template


def init_pages(apps, schema_editor):
    page_model = apps.get_model('block', 'Page')
    template_model = apps.get_model('block', 'Template')
    template_section_model = apps.get_model('block', 'TemplateSection')
    page_pks = [item.pk for item in page_model.objects.all()]
    for pk in page_pks:
        page = page_model.objects.get(pk=pk)
        template = init_template(page, template_model, template_section_model)
        page.template = template
        page.save()
    # mark un-used templates as deleted
    pages = page_model.objects.exclude(deleted=True).exclude(is_custom=True)
    template_pks = list(set([item.template.pk for item in pages]))
    template_model.objects.exclude(pk__in=template_pks).update(deleted=True)


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0009_auto_20151030_1153'),
    ]

    operations = [
        migrations.RunPython(init_pages),
    ]

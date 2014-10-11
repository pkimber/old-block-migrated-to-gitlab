# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def _create_state(model, slug):
    try:
        model.objects.get(slug=slug)
    except model.DoesNotExist:
        instance = model(**dict(name=slug, slug=slug))
        instance.save()
        instance.full_clean()


def default_state(apps, schema_editor):
    """Create default edit and moderation states.

    We can't import a model directly as it may be a newer version than this
    migration expects.  We use the historical version.

    """
    EditState = apps.get_model('block', 'EditState')
    _create_state(EditState, 'add')
    _create_state(EditState, 'edit')
    _create_state(EditState, 'push')
    ModerateState = apps.get_model("block", "EditState")
    _create_state(ModerateState, 'pending')
    _create_state(ModerateState, 'published')
    _create_state(ModerateState, 'removed')


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(default_state),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0008_auto_20151026_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='meta_description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='page',
            name='meta_keywords',
            field=models.TextField(blank=True),
        ),
    ]

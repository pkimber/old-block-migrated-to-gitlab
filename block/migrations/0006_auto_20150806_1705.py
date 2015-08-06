# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0005_linkdocument'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkdocument',
            name='title',
            field=models.CharField(default='Testing', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='linkdocument',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]

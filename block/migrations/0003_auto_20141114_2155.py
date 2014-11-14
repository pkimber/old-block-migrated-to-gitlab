# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0002_auto_20141011_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='block_app',
            field=models.CharField(help_text="app name e.g. 'compose'", max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='section',
            name='block_model',
            field=models.CharField(help_text="model name e.g. 'Article'", max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='section',
            name='create_url_name',
            field=models.CharField(help_text="url name for creating the model e.g. 'compose.article.create'", blank=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='section',
            name='slug',
            field=models.SlugField(help_text='What is this field used for?', unique=True, max_length=100),
            preserve_default=True,
        ),
    ]

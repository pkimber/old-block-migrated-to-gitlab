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
            field=models.TextField(help_text='Concise explanation of the contents of this page (used by search engines - optimal length 155 characters).', blank=True),
        ),
        migrations.AddField(
            model_name='page',
            name='meta_keywords',
            field=models.TextField(help_text='keywords for search engines', blank=True),
        ),
    ]

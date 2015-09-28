# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0006_auto_20150818_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='url_external',
            field=models.URLField(max_length=512, help_text='URL for a web site e.g. http://www.bbc.co.uk/news', verbose_name='Link', blank=True, null=True),
        ),
    ]

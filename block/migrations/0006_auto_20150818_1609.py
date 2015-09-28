# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0005_menu_menuitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='headerfooter',
            name='footer_left',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='headerfooter',
            name='footer_right',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='headerfooter',
            name='header',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]

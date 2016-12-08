# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-24 13:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0014_auto_20161014_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headerfooter',
            name='footer_left',
            field=models.TextField(blank=True, help_text='A block of text intended to be shown on the left side of the Footer below a heading '),
        ),
        migrations.AlterField(
            model_name='headerfooter',
            name='footer_right',
            field=models.TextField(blank=True, help_text='A block of text intended to be shown on the right side of the Footer below a heading '),
        ),
    ]
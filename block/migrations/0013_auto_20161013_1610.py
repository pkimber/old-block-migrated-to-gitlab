# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-13 15:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0012_auto_20160831_0058'),
    ]

    operations = [
        migrations.AddField(
            model_name='headerfooter',
            name='company_address',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='headerfooter',
            name='company_email',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='headerfooter',
            name='company_fax',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='headerfooter',
            name='company_hours',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='headerfooter',
            name='company_phone',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='headerfooter',
            name='footer_left_header',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='headerfooter',
            name='footer_right_header',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='headerfooter',
            name='google_analytics_code',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='headerfooter',
            name='google_map_lat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='headerfooter',
            name='google_map_long',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='headerfooter',
            name='google_map_zoom',
            field=models.PositiveIntegerField(default=17),
        ),
        migrations.AddField(
            model_name='headerfooter',
            name='google_verification_code',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]
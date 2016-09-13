# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-30 23:58
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('block', '0011_auto_20151030_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 8, 30, 23, 57, 21, 505426, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menu',
            name='date_deleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='menu',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='menu',
            name='modified',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 8, 30, 23, 57, 27, 305111, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menu',
            name='user_deleted',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 8, 30, 23, 57, 32, 712865, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menuitem',
            name='date_deleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='modified',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 8, 30, 23, 57, 38, 48518, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menuitem',
            name='user_deleted',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='block.Menu'),
        ),
    ]

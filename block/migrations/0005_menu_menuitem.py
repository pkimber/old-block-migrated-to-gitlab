# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0004_auto_20150810_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('slug', models.SlugField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('navigation', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Menu',
                'ordering': ('navigation', 'slug'),
                'verbose_name_plural': 'Menus',
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('slug', models.SlugField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('order', models.PositiveIntegerField(default=0)),
                ('link', models.ForeignKey(blank=True, to='block.Link', null=True)),
                ('menu', models.ForeignKey(to='block.Menu', null=True)),
                ('parent', models.ForeignKey(blank=True, to='block.MenuItem', null=True)),
            ],
            options={
                'verbose_name': 'Menu Item',
                'ordering': ('order', 'title'),
                'verbose_name_plural': 'Menu Items',
            },
        ),
    ]

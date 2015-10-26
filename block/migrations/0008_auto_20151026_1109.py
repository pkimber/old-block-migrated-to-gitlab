# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0007_auto_20150821_2228'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageCategory',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', django_extensions.db.fields.AutoSlugField(max_length=100, populate_from=('name',), unique=True, editable=False, blank=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Image Category',
                'ordering': ['name'],
                'verbose_name_plural': 'Image Categories',
            },
        ),
        migrations.CreateModel(
            name='LinkCategory',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', django_extensions.db.fields.AutoSlugField(max_length=100, populate_from=('name',), unique=True, editable=False, blank=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Link Category',
                'ordering': ['name'],
                'verbose_name_plural': 'Link Categories',
            },
        ),
        migrations.AddField(
            model_name='link',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='image',
            name='category',
            field=models.ForeignKey(to='block.ImageCategory', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='link',
            name='category',
            field=models.ForeignKey(to='block.LinkCategory', blank=True, null=True),
        ),
    ]

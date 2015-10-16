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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', django_extensions.db.fields.AutoSlugField(unique=True, populate_from=('name',), blank=True, editable=False, max_length=100)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Image Category',
                'verbose_name_plural': 'Image Categories',
            },
        ),
        migrations.AddField(
            model_name='image',
            name='category',
            field=models.ForeignKey(to='block.ImageCategory', blank=True, null=True),
        ),
    ]

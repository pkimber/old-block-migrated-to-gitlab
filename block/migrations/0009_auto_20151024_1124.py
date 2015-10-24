# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0008_auto_20151016_1955'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, max_length=100, blank=True, unique=True, populate_from=('name',))),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Link Categories',
                'verbose_name': 'Link Category',
            },
        ),
        migrations.AddField(
            model_name='link',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='link',
            name='category',
            field=models.ForeignKey(blank=True, to='block.LinkCategory', null=True),
        ),
    ]

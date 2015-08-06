# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0004_linkimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('document', models.FileField(upload_to='link/document')),
                ('description', models.TextField()),
                ('original_file_name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Link Document',
                'verbose_name_plural': 'Link Documents',
            },
        ),
    ]

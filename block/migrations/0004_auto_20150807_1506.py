# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0003_auto_20150419_2130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('document', models.FileField(blank=True, upload_to='link/document', help_text='Uploaded document e.g. PDF', null=True)),
                ('original_file_name', models.CharField(blank=True, max_length=100, help_text='Original file name of the document', null=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='link/image')),
                ('description', models.TextField()),
                ('alt_tag', models.CharField(max_length=100)),
                ('original_file_name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Link Image',
                'verbose_name_plural': 'Link Images',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('link_type', models.CharField(max_length=1, choices=[('d', 'Document'), ('p', 'Page'), ('u', 'External URL'), ('r', 'Internal URL')])),
                ('url_external', models.URLField(blank=True, verbose_name='Link', help_text='URL for a web site e.g. http://www.bbc.co.uk/news', null=True)),
                ('document', models.ForeignKey(blank=True, null=True, to='block.Document')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, help_text="e.g. 'project.page' or 'web.training.application'")),
                ('arg1', models.SlugField(max_length=100, help_text="e.g. 'training'")),
                ('arg2', models.SlugField(max_length=100, help_text="e.g. 'application'")),
            ],
            options={
                'verbose_name': 'URL',
                'verbose_name_plural': 'URL',
            },
        ),
        migrations.AddField(
            model_name='link',
            name='url_internal',
            field=models.ForeignKey(blank=True, null=True, to='block.Url'),
        ),
    ]

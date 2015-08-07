# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0003_auto_20150419_2130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('link_type', models.CharField(max_length=1, choices=[('d', 'Document'), ('p', 'Page'), ('u', 'External URL'), ('r', 'Internal URL')])),
                ('document', models.FileField(null=True, upload_to='link/document', help_text='Uploaded document e.g. PDF', blank=True)),
                ('document_file_name', models.CharField(null=True, max_length=100, help_text='Original file name of the document', blank=True)),
                ('url_external', models.URLField(verbose_name='Link', null=True, help_text='URL for a web site e.g. http://www.bbc.co.uk/news', blank=True)),
                ('url_internal', models.TextField(verbose_name='Link text', help_text="URL name for use with 'reverse' e.g. 'cms.page.list'", blank=True)),
                ('page', models.ForeignKey(help_text='Page on the site', null=True, blank=True, to='block.Page')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
        ),
        migrations.CreateModel(
            name='LinkImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
    ]

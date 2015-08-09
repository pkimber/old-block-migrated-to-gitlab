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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('document', models.FileField(upload_to='link/document', help_text='Uploaded document e.g. PDF', null=True, blank=True)),
                ('original_file_name', models.CharField(max_length=100, help_text='Original file name of the document', null=True, blank=True)),
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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='link/image')),
                ('alt', models.CharField(max_length=100, help_text='Alternate text for an image (if the image cannot be displayed)')),
                ('original_file_name', models.CharField(max_length=100)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Link Image',
                'verbose_name_plural': 'Link Images',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250)),
                ('link_type', models.CharField(max_length=1, choices=[('d', 'Document'), ('u', 'External URL'), ('r', 'Internal URL')])),
                ('url_external', models.URLField(help_text='URL for a web site e.g. http://www.bbc.co.uk/news', null=True, verbose_name='Link', blank=True)),
                ('document', models.ForeignKey(to='block.Document', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('url_type', models.CharField(max_length=1, choices=[('p', 'Page'), ('r', 'Reverse')])),
                ('name', models.CharField(max_length=100, help_text="e.g. 'project.page' or 'web.training.application'")),
                ('arg1', models.SlugField(max_length=100, help_text="e.g. 'training'")),
                ('arg2', models.SlugField(max_length=100, help_text="e.g. 'application'")),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'URLs',
                'verbose_name': 'URL',
            },
        ),
        migrations.AlterUniqueTogether(
            name='url',
            unique_together=set([('name', 'arg1', 'arg2')]),
        ),
        migrations.AddField(
            model_name='link',
            name='url_internal',
            field=models.ForeignKey(help_text='A page on this web site', to='block.Url', null=True, blank=True),
        ),
    ]

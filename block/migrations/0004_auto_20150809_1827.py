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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('document', models.FileField(null=True, blank=True, help_text='Uploaded document e.g. PDF', upload_to='link/document')),
                ('original_file_name', models.CharField(null=True, blank=True, help_text='Original file name of the document', max_length=100)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Documents',
                'verbose_name': 'Document',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='link/image')),
                ('alt', models.CharField(help_text='Alternate text for an image (if the image cannot be displayed)', max_length=100)),
                ('original_file_name', models.CharField(max_length=100)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Link Images',
                'verbose_name': 'Link Image',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250)),
                ('link_type', models.CharField(choices=[('d', 'Document'), ('u', 'External URL'), ('r', 'Internal URL')], max_length=1)),
                ('url_external', models.URLField(null=True, verbose_name='Link', blank=True, help_text='URL for a web site e.g. http://www.bbc.co.uk/news')),
                ('document', models.ForeignKey(to='block.Document', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Links',
                'verbose_name': 'Link',
            },
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('url_type', models.CharField(choices=[('p', 'Page'), ('r', 'Reverse')], max_length=1)),
                ('name', models.CharField(help_text="e.g. 'project.page' or 'web.training.application'", max_length=100)),
                ('arg1', models.SlugField(help_text="e.g. 'training'", max_length=100)),
                ('arg2', models.SlugField(help_text="e.g. 'application'", max_length=100)),
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
            field=models.ForeignKey(to='block.Url', null=True, blank=True, help_text='A page on this web site'),
        ),
    ]

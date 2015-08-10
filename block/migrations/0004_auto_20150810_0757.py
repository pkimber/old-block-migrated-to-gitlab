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
                ('document', models.FileField(null=True, upload_to='link/document', blank=True, help_text='Uploaded document e.g. PDF')),
                ('original_file_name', models.CharField(max_length=100, null=True, blank=True, help_text='Original file name of the document')),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Documents',
                'verbose_name': 'Document',
            },
        ),
        migrations.CreateModel(
            name='HeaderFooter',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('header', models.CharField(max_length=150)),
                ('url_twitter', models.URLField(verbose_name='Twitter URL', blank=True)),
                ('url_linkedin', models.URLField(verbose_name='LinkedIn URL', blank=True)),
                ('url_facebook', models.URLField(verbose_name='Facebook URL', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Header and footers',
                'verbose_name': 'Header and footer',
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
                'verbose_name_plural': 'Link Images',
                'verbose_name': 'Link Image',
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
                ('url_external', models.URLField(null=True, verbose_name='Link', blank=True, help_text='URL for a web site e.g. http://www.bbc.co.uk/news')),
                ('document', models.ForeignKey(to='block.Document', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Links',
                'verbose_name': 'Link',
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('template_name', models.CharField(max_length=150, help_text="File name e.g. 'compose/page_article.html'")),
            ],
            options={
                'ordering': ('template_name',),
                'verbose_name_plural': 'Templates',
                'verbose_name': 'Template',
            },
        ),
        migrations.CreateModel(
            name='TemplateSection',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('section', models.ForeignKey(to='block.Section')),
                ('template', models.ForeignKey(to='block.Template')),
            ],
            options={
                'ordering': ('template__template_name', 'section__name'),
                'verbose_name_plural': 'Template sections',
                'verbose_name': 'Template section',
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
            field=models.ForeignKey(to='block.Url', blank=True, help_text='A page on this web site', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='templatesection',
            unique_together=set([('template', 'section')]),
        ),
    ]

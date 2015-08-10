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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('document', models.FileField(help_text='Uploaded document e.g. PDF', null=True, upload_to='link/document', blank=True)),
                ('original_file_name', models.CharField(help_text='Original file name of the document', null=True, max_length=100, blank=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='link/image')),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250)),
                ('link_type', models.CharField(max_length=1, choices=[('d', 'Document'), ('u', 'External URL'), ('r', 'Internal URL')])),
                ('url_external', models.URLField(verbose_name='Link', help_text='URL for a web site e.g. http://www.bbc.co.uk/news', null=True, blank=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('template_name', models.CharField(help_text="File name e.g. 'compose/page_article.html'", max_length=150)),
            ],
            options={
                'verbose_name_plural': 'Templates',
                'verbose_name': 'Template',
                'ordering': ('template_name',),
            },
        ),
        migrations.CreateModel(
            name='TemplateSection',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('section', models.ForeignKey(to='block.Section')),
                ('template', models.ForeignKey(to='block.Template')),
            ],
            options={
                'verbose_name_plural': 'Template sections',
                'verbose_name': 'Template section',
                'ordering': ('template__template_name', 'section__name'),
            },
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('url_type', models.CharField(max_length=1, choices=[('p', 'Page'), ('r', 'Reverse')])),
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
            field=models.ForeignKey(to='block.Url', blank=True, help_text='A page on this web site', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='templatesection',
            unique_together=set([('template', 'section')]),
        ),
    ]

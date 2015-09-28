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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('document', models.FileField(help_text='Uploaded document e.g. PDF', null=True, blank=True, upload_to='link/document')),
                ('original_file_name', models.CharField(help_text='Original file name of the document', null=True, blank=True, max_length=100)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
        ),
        migrations.CreateModel(
            name='HeaderFooter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('header', models.CharField(max_length=150)),
                ('url_twitter', models.URLField(verbose_name='Twitter URL', blank=True)),
                ('url_linkedin', models.URLField(verbose_name='LinkedIn URL', blank=True)),
                ('url_facebook', models.URLField(verbose_name='Facebook URL', blank=True)),
            ],
            options={
                'verbose_name': 'Header and footer',
                'verbose_name_plural': 'Header and footers',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='link/image')),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250)),
                ('link_type', models.CharField(choices=[('d', 'Document'), ('u', 'External URL'), ('r', 'Internal URL')], max_length=1)),
                ('url_external', models.URLField(help_text='URL for a web site e.g. http://www.bbc.co.uk/news', null=True, verbose_name='Link', blank=True)),
                ('document', models.ForeignKey(null=True, blank=True, to='block.Document')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('template_name', models.CharField(help_text="File name e.g. 'compose/page_article.html'", max_length=150)),
            ],
            options={
                'verbose_name': 'Template',
                'ordering': ('template_name',),
                'verbose_name_plural': 'Templates',
            },
        ),
        migrations.CreateModel(
            name='TemplateSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('section', models.ForeignKey(to='block.Section')),
                ('template', models.ForeignKey(to='block.Template')),
            ],
            options={
                'verbose_name': 'Template section',
                'ordering': ('template__template_name', 'section__name'),
                'verbose_name_plural': 'Template sections',
            },
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('url_type', models.CharField(choices=[('p', 'Page'), ('r', 'Reverse')], max_length=1)),
                ('name', models.CharField(help_text="e.g. 'project.page' or 'web.training.application'", max_length=100)),
                ('arg1', models.SlugField(help_text="e.g. 'training'", max_length=100)),
                ('arg2', models.SlugField(help_text="e.g. 'application'", max_length=100)),
                ('arg3', models.SlugField(help_text="e.g. 'urgent'", max_length=100)),
                ('deleted', models.BooleanField(default=False)),
                ('page', models.ForeignKey(null=True, blank=True, to='block.Page')),
            ],
            options={
                'verbose_name': 'URL',
                'verbose_name_plural': 'URLs',
            },
        ),
        migrations.AddField(
            model_name='link',
            name='url_internal',
            field=models.ForeignKey(null=True, blank=True, help_text='A page on this web site', to='block.Url'),
        ),
        migrations.AlterUniqueTogether(
            name='url',
            unique_together=set([('page', 'name', 'arg1', 'arg2', 'arg3')]),
        ),
        migrations.AlterUniqueTogether(
            name='templatesection',
            unique_together=set([('template', 'section')]),
        ),
    ]

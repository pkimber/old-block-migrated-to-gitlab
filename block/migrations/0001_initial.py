# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EditState',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Edit state',
                'ordering': ['name'],
                'verbose_name': 'Edit state',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModerateState',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Moderated',
                'ordering': ['name'],
                'verbose_name': 'Moderate',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('slug_menu', models.SlugField(blank=True, max_length=100)),
                ('order', models.IntegerField(default=0)),
                ('is_home', models.BooleanField(default=False)),
                ('template_name', models.CharField(max_length=150)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Pages',
                'ordering': ['order', 'slug', 'slug_menu'],
                'verbose_name': 'Page',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageSection',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('page', models.ForeignKey(to='block.Page')),
            ],
            options={
                'verbose_name_plural': 'Page sections',
                'ordering': ('page__slug', 'section__slug'),
                'verbose_name': 'Page section',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaginatedSection',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('items_per_page', models.IntegerField(default=10)),
                ('order_by_field', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('block_app', models.CharField(max_length=100, help_text="app name e.g. 'compose'")),
                ('block_model', models.CharField(max_length=100, help_text="model name e.g. 'Article'")),
                ('create_url_name', models.CharField(blank=True, max_length=100, help_text="url name for creating the model e.g. 'compose.article.create'")),
                ('paginated', models.ForeignKey(blank=True, to='block.PaginatedSection', null=True)),
            ],
            options={
                'verbose_name_plural': 'Sections',
                'ordering': ('name',),
                'verbose_name': 'Section',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pagesection',
            name='section',
            field=models.ForeignKey(to='block.Section'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='pagesection',
            unique_together=set([('page', 'section')]),
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('slug', 'slug_menu')]),
        ),
    ]

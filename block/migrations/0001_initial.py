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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Edit state',
                'verbose_name_plural': 'Edit state',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModerateState',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Moderate',
                'verbose_name_plural': 'Moderated',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('slug_menu', models.SlugField(max_length=100, blank=True)),
                ('order', models.IntegerField(default=0)),
                ('is_home', models.BooleanField(default=False)),
                ('template_name', models.CharField(max_length=150)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['order', 'slug', 'slug_menu'],
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageSection',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('page', models.ForeignKey(to='block.Page')),
            ],
            options={
                'ordering': ('page__slug', 'section__slug'),
                'verbose_name': 'Page section',
                'verbose_name_plural': 'Page sections',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaginatedSection',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('block_app', models.CharField(max_length=100)),
                ('block_model', models.CharField(max_length=100)),
                ('create_url_name', models.CharField(max_length=100, blank=True)),
                ('paginated', models.ForeignKey(null=True, to='block.PaginatedSection', blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
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

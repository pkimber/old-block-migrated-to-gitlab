# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0008_auto_20151026_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='meta_description',
            field=models.TextField(help_text='Concise explanation of the contents of this page (used by search engines - optimal length 155 characters).', blank=True),
        ),
        migrations.AddField(
            model_name='page',
            name='meta_keywords',
            field=models.TextField(help_text='keywords for search engines', blank=True),
        ),
        migrations.AddField(
            model_name='page',
            name='template',
            field=models.ForeignKey(to='block.Template', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='template',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='template',
            name='name',
            field=models.CharField(max_length=100, default='Example Template Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='template',
            name='template_name',
            field=models.CharField(help_text="File name e.g. 'compose/page_article.html'", unique=True, max_length=150),
        ),
    ]

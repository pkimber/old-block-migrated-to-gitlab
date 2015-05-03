# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import block.models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0003_auto_20150419_2130'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('date_moderated', models.DateTimeField(null=True, blank=True)),
                ('order', models.IntegerField()),
                ('title', models.TextField()),
                ('picture', models.ImageField(blank=True, upload_to='block')),
            ],
            options={
                'verbose_name': 'Test content',
                'verbose_name_plural': 'Test contents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TitleBlock',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('page_section', models.ForeignKey(to='block.PageSection')),
            ],
            options={
                'verbose_name': 'Block',
                'verbose_name_plural': 'Blocks',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='title',
            name='block',
            field=models.ForeignKey(to='example_block.TitleBlock', related_name='content'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='title',
            name='edit_state',
            field=models.ForeignKey(to='block.EditState', default=block.models._default_edit_state),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='title',
            name='moderate_state',
            field=models.ForeignKey(to='block.ModerateState', default=block.models._default_moderate_state),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='title',
            name='user_moderated',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, related_name='+'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='title',
            unique_together=set([('block', 'moderate_state')]),
        ),
    ]

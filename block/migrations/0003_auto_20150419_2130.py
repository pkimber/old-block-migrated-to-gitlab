# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('block', '0002_auto_20141011_2223'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewUrl',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('url', models.CharField(max_length=200, blank=True)),
                ('page', models.ForeignKey(to='block.Page')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+')),
            ],
            options={
                'ordering': ('user__username', 'page__slug', 'page__slug_menu'),
                'verbose_name_plural': 'View URLs',
                'verbose_name': 'View URL',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='viewurl',
            unique_together=set([('user', 'page')]),
        ),
        migrations.AddField(
            model_name='page',
            name='is_custom',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

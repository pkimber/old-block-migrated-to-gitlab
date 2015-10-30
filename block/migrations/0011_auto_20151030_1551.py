# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0010_auto_20151029_1927'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='template_name',
        ),
        migrations.AlterField(
            model_name='page',
            name='order',
            field=models.IntegerField(help_text='Menu order (set to 0 to hide)'),
        ),
        migrations.AlterField(
            model_name='page',
            name='template',
            field=models.ForeignKey(to='block.Template'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-13 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20171112_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='random'),
            preserve_default=False,
        ),
    ]

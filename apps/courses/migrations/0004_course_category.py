# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-08-24 21:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20170824_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default='', max_length=20, verbose_name='\u8bfe\u7a0b\u7c7b\u522b'),
        ),
    ]

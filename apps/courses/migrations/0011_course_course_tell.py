# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-08-25 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20170824_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_tell',
            field=models.CharField(default='', max_length=100, verbose_name='\u8bfe\u7a0b\u516c\u544a'),
        ),
    ]

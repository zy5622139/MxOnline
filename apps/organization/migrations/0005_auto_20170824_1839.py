# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-08-24 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20170823_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image/teacher/%Y/%m', verbose_name='\u5c01\u9762\u56fe'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='image',
            field=models.ImageField(upload_to='image/course_org/%Y/%m', verbose_name='\u5c01\u9762\u56fe'),
        ),
    ]
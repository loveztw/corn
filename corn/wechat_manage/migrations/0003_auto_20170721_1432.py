# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-21 06:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat_manage', '0002_auto_20170721_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='updatedate',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='updatedate',
            field=models.DateTimeField(),
        ),
    ]

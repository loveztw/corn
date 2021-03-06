# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-21 06:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wechat_manage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='createdate',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='role',
            name='updatedate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='createdate',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='updatedate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='userrole',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wechat_manage.role'),
        ),
    ]

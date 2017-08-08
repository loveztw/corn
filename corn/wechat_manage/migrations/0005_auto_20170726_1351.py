# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-26 05:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wechat_manage', '0004_projectinfo_userlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='userrole',
        ),
        migrations.AddField(
            model_name='userlist',
            name='roleid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wechat_manage.role'),
        ),
    ]

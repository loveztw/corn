# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-19 09:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rolename', models.CharField(max_length=32)),
                ('ability', models.CharField(max_length=32, null=True)),
                ('createdate', models.DateField()),
                ('updatedate', models.DateField()),
                ('deleteflag', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='userInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('mailaddress', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=128)),
                ('createdate', models.DateField()),
                ('updatedate', models.DateField()),
                ('deleteflag', models.CharField(max_length=1)),
                ('userrole', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wechat_manage.role')),
            ],
        ),
    ]

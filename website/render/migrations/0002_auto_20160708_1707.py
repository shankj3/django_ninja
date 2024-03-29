# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-09 00:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('render', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Templates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_name', models.CharField(max_length=100)),
                ('template_body', models.CharField(max_length=10000)),
            ],
        ),
        migrations.AddField(
            model_name='rendered',
            name='templates_used',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]

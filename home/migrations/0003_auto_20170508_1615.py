# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-08 16:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20170507_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crowdedness',
            name='when',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-13 08:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_live'),
    ]

    operations = [
        migrations.CreateModel(
            name='Noise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(auto_now_add=True, verbose_name=b'timestamp')),
                ('mag', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Wifi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(auto_now_add=True, verbose_name=b'timestamp')),
                ('mag', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='live',
        ),
    ]
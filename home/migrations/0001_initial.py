# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-28 13:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ministry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('day', models.PositiveSmallIntegerField()),
                ('address1', models.CharField(max_length=50)),
                ('address2', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zip', models.CharField(max_length=50)),
            ],
        ),
    ]

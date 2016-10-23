# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-04 09:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20160801_1841'),
    ]

    operations = [
        migrations.CreateModel(
            name='Denomination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ministries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ministry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='last_name',
        ),
        migrations.AddField(
            model_name='church',
            name='helped',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='church',
            name='number',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='church',
            name='peopleNeeded',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='number',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='church',
            name='address1',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='church',
            name='address2',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='church',
            name='city',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='church',
            name='end',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='church',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='church',
            name='start',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='church',
            name='state',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='church',
            name='zip',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]

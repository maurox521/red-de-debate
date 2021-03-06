# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-24 17:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Argumento',
            fields=[
                ('id_argument', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=300)),
                ('position', models.IntegerField(default=1)),
                ('owner_type', models.CharField(default='username', max_length=50)),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Counterargument',
            fields=[
                ('id_counterarg', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=300)),
                ('owner_type', models.CharField(default='username', max_length=50)),
                ('date', models.DateField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id_position', models.AutoField(primary_key=True, serialize=False)),
                ('position', models.IntegerField(default=1)),
                ('change', models.IntegerField(default=0)),
                ('count_change', models.IntegerField(default=0)),
                ('date', models.DateField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='PrivateMembers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id_rate', models.AutoField(primary_key=True, serialize=False)),
                ('rate_type', models.CharField(default='none', max_length=50)),
                ('date', models.DateField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('num', models.IntegerField(default=1)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]

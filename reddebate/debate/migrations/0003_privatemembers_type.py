# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-25 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debate', '0002_auto_20180924_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='privatemembers',
            name='type',
            field=models.CharField(default='username', max_length=50),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-24 17:06
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Debate',
            fields=[
                ('id_debate', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=1000)),
                ('date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('end_date', models.DateField(blank=True, default=None, null=True)),
                ('owner_type', models.CharField(default='username', max_length=50)),
                ('length', models.IntegerField(blank=True, default=300)),
                ('state', models.CharField(default='open', max_length=20)),
                ('args_max', models.IntegerField(default=1)),
                ('position_max', models.IntegerField(default=3)),
                ('counterargs_max', models.IntegerField(default=1)),
                ('counterargs_type', models.IntegerField(default=0)),
                ('members_type', models.IntegerField(default=0)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-24 17:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('resumen', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('debate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='id_debate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumen.Debate'),
        ),
        migrations.AddField(
            model_name='visit',
            name='id_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rate',
            name='id_argument',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='debate.Argumento'),
        ),
        migrations.AddField(
            model_name='rate',
            name='id_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='privatemembers',
            name='id_debate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumen.Debate'),
        ),
        migrations.AddField(
            model_name='privatemembers',
            name='id_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='position',
            name='id_debate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumen.Debate'),
        ),
        migrations.AddField(
            model_name='position',
            name='id_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='counterargument',
            name='id_argument',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='debate.Argumento'),
        ),
        migrations.AddField(
            model_name='counterargument',
            name='id_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='argumento',
            name='id_debate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumen.Debate'),
        ),
        migrations.AddField(
            model_name='argumento',
            name='id_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

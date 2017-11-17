# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-09 21:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greenhouse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='graph_range_detailed',
            field=models.IntegerField(default=48, verbose_name='Graph range detailed (hours)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='setting',
            name='graph_range_normal',
            field=models.IntegerField(default=10, verbose_name='Graph range normal (hours)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='datapoint',
            name='image',
            field=models.ImageField(upload_to='media/img'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-13 11:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('greenhouse', '0005_setting_self_regulate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setting',
            name='settings_profile',
        ),
    ]
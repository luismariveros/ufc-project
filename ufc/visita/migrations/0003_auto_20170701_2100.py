# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 01:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visita', '0002_auto_20170701_1753'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Persona',
            new_name='Visita',
        ),
    ]
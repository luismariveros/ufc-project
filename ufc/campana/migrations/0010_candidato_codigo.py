# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-25 16:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campana', '0009_remove_persona_permiso'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidato',
            name='codigo',
            field=models.CharField(default='', max_length=20),
        ),
    ]

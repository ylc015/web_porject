# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-10 00:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Relationship',
            new_name='Relationships',
        ),
    ]

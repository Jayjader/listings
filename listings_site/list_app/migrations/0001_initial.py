# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_edit_date', models.DateTimeField(verbose_name='date last edited')),
                ('title', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=500)),
                ('creator_email', models.CharField(max_length=100)),
                ('edit_token', models.CharField(max_length=16)),
            ],
        ),
    ]

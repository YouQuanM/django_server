# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-01 22:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poker_cards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poker_username', models.CharField(max_length=64)),
                ('poker_card_color', models.IntegerField()),
                ('poker_card_num', models.IntegerField()),
            ],
        ),
    ]

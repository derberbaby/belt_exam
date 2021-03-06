# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-28 17:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('belt_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('plan', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('party_people', models.ManyToManyField(related_name='trips', to='belt_app.User')),
                ('planned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='belt_app.User')),
            ],
        ),
    ]

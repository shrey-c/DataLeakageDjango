# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-11 17:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=b'null', max_length=50)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('accesslevel', models.CharField(default=4, max_length=50)),
                ('document', models.FileField(upload_to=b'documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

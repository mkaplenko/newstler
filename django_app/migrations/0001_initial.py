# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-26 22:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMetaInformationModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.TextField(blank=True, null=True, verbose_name='linkedIn access token')),
                ('expiration', models.DateTimeField(blank=True, null=True, verbose_name='Token expiration')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='meta', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
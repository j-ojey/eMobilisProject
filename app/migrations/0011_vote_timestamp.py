# Generated by Django 5.0.7 on 2024-12-10 21:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_profile_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]

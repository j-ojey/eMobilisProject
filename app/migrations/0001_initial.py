# Generated by Django 5.1.3 on 2024-11-30 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=25)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=25)),
                ('email', models.CharField(max_length=25)),
                ('password', models.CharField(max_length=128)),
                ('confirm_password', models.CharField(max_length=128)),
                ('age', models.IntegerField(null=True)),
            ],
        ),
    ]

# Generated by Django 3.1.8 on 2021-06-17 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_is_scheduler'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_scheduler',
        ),
    ]

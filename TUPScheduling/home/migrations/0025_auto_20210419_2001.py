# Generated by Django 3.1.8 on 2021-04-19 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_auto_20210419_1935'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rooms',
            options={'ordering': ['Room_Name'], 'verbose_name': 'Rooms', 'verbose_name_plural': 'Rooms'},
        ),
    ]
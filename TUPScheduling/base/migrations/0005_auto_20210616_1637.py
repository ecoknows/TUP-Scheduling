# Generated by Django 3.1.8 on 2021-06-16 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20210615_1905'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProfessorsSchedule',
        ),
        migrations.DeleteModel(
            name='RoomsSchedule',
        ),
        migrations.DeleteModel(
            name='SectionsSchedule',
        ),
    ]

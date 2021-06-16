# Generated by Django 3.1.8 on 2021-06-16 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_schedule_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='starting_time',
            field=models.CharField(choices=[(7, '07:00 - 08:00'), (8, '08:00 - 09:00'), (9, '09:00 - 10:00'), (10, '10:00 - 11:00'), (11, '11:00 - 12:00'), (12, '12:00 - 01:00'), (1, '01:00 - 02:00'), (2, '02:00 - 03:00'), (3, '03:00 - 04:00'), (4, '04:00 - 05:00'), (5, '05:00 - 06:00'), (6, '06:00 - 07:00')], max_length=200, null=True),
        ),
    ]

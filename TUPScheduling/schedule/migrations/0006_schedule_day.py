# Generated by Django 3.1.8 on 2021-06-16 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_auto_20210615_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='day',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], max_length=20, null=True),
        ),
    ]

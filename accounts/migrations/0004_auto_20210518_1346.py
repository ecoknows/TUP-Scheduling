# Generated by Django 3.1.8 on 2021-05-18 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210518_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professorsaccount',
            name='scheduler',
            field=models.CharField(choices=[('professor', 'Professor'), ('scheduler', 'Scheduler')], default='', max_length=20, null=True),
        ),
    ]
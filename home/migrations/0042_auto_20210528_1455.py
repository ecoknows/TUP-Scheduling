# Generated by Django 3.1.8 on 2021-05-28 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_auto_20210528_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulksections',
            name='first_year',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='bulksections',
            name='fourth_year',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='bulksections',
            name='ns_first_year',
            field=models.IntegerField(default=0, null=True, verbose_name='First Year'),
        ),
        migrations.AlterField(
            model_name='bulksections',
            name='ns_fourth_year',
            field=models.IntegerField(default=0, null=True, verbose_name='Fourth Year'),
        ),
        migrations.AlterField(
            model_name='bulksections',
            name='ns_second_year',
            field=models.IntegerField(default=0, null=True, verbose_name='Second Year'),
        ),
        migrations.AlterField(
            model_name='bulksections',
            name='ns_third_year',
            field=models.IntegerField(default=0, null=True, verbose_name='Third Year'),
        ),
        migrations.AlterField(
            model_name='bulksections',
            name='second_year',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='bulksections',
            name='third_year',
            field=models.IntegerField(default=0, null=True),
        ),
    ]

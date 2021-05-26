# Generated by Django 3.1.8 on 2021-05-26 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0035_auto_20210526_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='sections',
            name='course_name',
            field=models.CharField(help_text='Ex. BSCS', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='sections',
            name='first_year',
            field=models.CharField(default=0, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='sections',
            name='fourth_year',
            field=models.CharField(default=0, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='sections',
            name='ns_first_year',
            field=models.CharField(default=0, max_length=256, null=True, verbose_name='First Year'),
        ),
        migrations.AddField(
            model_name='sections',
            name='ns_fourth_year',
            field=models.CharField(default=0, max_length=256, null=True, verbose_name='Fourth Year'),
        ),
        migrations.AddField(
            model_name='sections',
            name='ns_second_year',
            field=models.CharField(default=0, max_length=256, null=True, verbose_name='Second Year'),
        ),
        migrations.AddField(
            model_name='sections',
            name='ns_third_year',
            field=models.CharField(default=0, max_length=256, null=True, verbose_name='Third Year'),
        ),
        migrations.AddField(
            model_name='sections',
            name='second_year',
            field=models.CharField(default=0, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='sections',
            name='third_year',
            field=models.CharField(default=0, max_length=256, null=True),
        ),
    ]

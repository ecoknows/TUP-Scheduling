# Generated by Django 3.1.8 on 2021-04-16 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_subjectsorderable_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(help_text='Ex. Rm. 202', max_length=10)),
                ('room_type', models.CharField(choices=[('Laboratory', 'Laboratory'), ('Lecture', 'Lecture')], max_length=20)),
            ],
        ),
    ]
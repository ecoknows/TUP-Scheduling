# Generated by Django 3.1.8 on 2021-06-03 08:23

import accounts.models
from django.db import migrations, models
import wagtail.search.index


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Professors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Ex. John', max_length=300, null=True)),
                ('middle_name', models.CharField(help_text='Ex. Michael', max_length=1, null=True)),
                ('last_name', models.CharField(help_text='Ex. Doe', max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('preferred_start_time', models.TimeField(blank=True, default=' 7:00 AM', help_text='At least 7:00 A.M.', null=True, validators=[accounts.models.Professors.validate_start_time])),
                ('preferred_end_time', models.TimeField(blank=True, default=' 7:00 PM', help_text='At most 7:00 P.M.', null=True, validators=[accounts.models.Professors.validate_end_time])),
                ('status', models.CharField(choices=[('Regular', 'Regular'), ('Part-time', 'Part-time')], default='Regular', max_length=200)),
            ],
            options={
                'verbose_name': 'Professor',
                'verbose_name_plural': 'Professors',
                'ordering': ['last_name'],
            },
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Ex. John', max_length=300, null=True)),
                ('middle_name', models.CharField(help_text='Ex. Michael', max_length=1, null=True)),
                ('last_name', models.CharField(help_text='Ex. Doe', max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
    ]

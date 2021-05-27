# Generated by Django 3.1.8 on 2021-05-18 06:46

import accounts.models
from django.db import migrations, models
import django.db.models.deletion
import wagtail.search.index


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_auto_20210518_1317'),
        ('accounts', '0004_auto_20210518_1346'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Ex. John', max_length=300, null=True)),
                ('middle_name', models.CharField(help_text='Ex. Michael', max_length=300, null=True)),
                ('last_name', models.CharField(help_text='Ex. Doe', max_length=300, null=True)),
                ('preferred_start_time', models.TimeField(blank=True, default=' 7:00 AM', help_text='At least 7:00 A.M.', null=True, validators=[accounts.models.Professors.validate_start_time])),
                ('preferred_end_time', models.TimeField(blank=True, default=' 7:00 PM', help_text='At most 7:00 P.M.', null=True, validators=[accounts.models.Professors.validate_end_time])),
                ('status', models.CharField(choices=[('Regular', 'Regular'), ('Part-time', 'Part-time')], default='Regular', max_length=200)),
                ('choose_department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.departments')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.sections')),
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
                ('middle_name', models.CharField(help_text='Ex. Michael', max_length=300, null=True)),
                ('last_name', models.CharField(help_text='Ex. Doe', max_length=300, null=True)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.sections')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
        migrations.RemoveField(
            model_name='studentsaccount',
            name='section',
        ),
        migrations.DeleteModel(
            name='ProfessorsAccount',
        ),
        migrations.DeleteModel(
            name='StudentsAccount',
        ),
    ]
# Generated by Django 3.1.8 on 2021-04-19 15:54

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import home.models
import modelcluster.fields
import wagtail.search.index


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0060_fix_workflow_unique_constraint'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminsAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Colleges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college_name', models.CharField(max_length=300, null=True)),
            ],
            options={
                'verbose_name': 'College',
                'verbose_name_plural': 'Colleges',
                'ordering': ['college_name'],
            },
        ),
        migrations.CreateModel(
            name='CourseCurriculum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(help_text='Ex. CS33', max_length=300, null=True)),
                ('starting_year', models.PositiveIntegerField(help_text='Use the following format: <YYYY>', null=True, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2020)])),
                ('ending_year', models.PositiveIntegerField(help_text='Use the following format: <YYYY>', null=True, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2020)])),
            ],
            options={
                'verbose_name': 'Course Curriculum',
                'verbose_name_plural': 'Course Curriculum',
                'ordering': ['course_name'],
            },
        ),
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Department_Name', models.CharField(help_text='Department of Mathematics', max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
                'ordering': ['Department_Name'],
            },
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='LoginPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Professors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Ex. John', max_length=300, null=True)),
                ('middle_name', models.CharField(help_text='Ex. Michael', max_length=300, null=True)),
                ('last_name', models.CharField(help_text='Ex. Doe', max_length=300, null=True)),
                ('preferred_start_time', models.TimeField(blank=True, help_text='At least 7:00', null=True, validators=[home.models.Professors.validate_start_time])),
                ('preferred_end_time', models.TimeField(blank=True, help_text='At most 19:00', null=True, validators=[home.models.Professors.validate_end_time])),
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
            name='ProfessorsAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ProfessorsSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Room_Name', models.CharField(help_text='Ex. CS33', max_length=20, null=True)),
                ('Room_Type', models.CharField(choices=[('Laboratory', 'Laboratory'), ('Lecture', 'Lecture')], default='Laboratory', max_length=50)),
            ],
            options={
                'verbose_name': 'Rooms',
                'verbose_name_plural': 'Rooms',
                'ordering': ['Room_Name'],
            },
        ),
        migrations.CreateModel(
            name='RoomsSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Sections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SectionsSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='StudentsAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_code', models.CharField(help_text='Ex. CS33', max_length=200, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('units', models.IntegerField(default=1)),
                ('lab_or_lec', models.CharField(choices=[('Laboratory', 'Laboratory'), ('Lecture', 'Lecture')], default='Laboratory', max_length=200)),
                ('sem', models.CharField(choices=[('First', 'First'), ('Second', 'Second')], default='First', max_length=200)),
                ('hours', models.FloatField(default=1)),
            ],
            options={
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
                'ordering': ['subject_code'],
            },
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
        migrations.CreateModel(
            name='SubjectsOrderable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('course_curriculum_model', modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_curriculum_parental_key', to='home.coursecurriculum')),
                ('professor_model', modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='professor_parental_key', to='home.professors')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.subjects')),
                ('subject_model', modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subject_parental_key', to='home.subjects')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RoomOrderable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.rooms')),
                ('room_model', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_parental_key', to='home.departments')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]

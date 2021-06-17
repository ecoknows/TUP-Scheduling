# Generated by Django 3.1.8 on 2021-06-17 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20210616_1637'),
        ('accounts', '0010_students_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='choose_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='base.departments'),
        ),
    ]
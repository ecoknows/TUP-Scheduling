# Generated by Django 3.1.8 on 2021-04-14 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_subjectsorderable'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectsorderable',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.subjects'),
        ),
    ]
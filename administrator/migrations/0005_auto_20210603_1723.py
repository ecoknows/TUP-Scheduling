# Generated by Django 3.1.8 on 2021-06-03 09:23

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0004_auto_20210603_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjectsorderable',
            name='co_requisite',
            field=modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='co_requisite', to='administrator.subjects'),
        ),
        migrations.AlterField(
            model_name='subjectsorderable',
            name='pre_requisite',
            field=modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pre_requisite', to='administrator.subjects'),
        ),
    ]

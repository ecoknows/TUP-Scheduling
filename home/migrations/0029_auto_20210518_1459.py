# Generated by Django 3.1.8 on 2021-05-18 06:59

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210518_1446'),
        ('home', '0028_auto_20210518_1317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professororderable',
            name='professor',
        ),
        migrations.AlterField(
            model_name='subjectsorderable',
            name='professor_model',
            field=modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='professor_parental_key', to='accounts.professors'),
        ),
        migrations.DeleteModel(
            name='Professors',
        ),
    ]
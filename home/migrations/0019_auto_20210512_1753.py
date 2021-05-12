# Generated by Django 3.1.8 on 2021-05-12 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20210512_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professors',
            name='choose_department',
            field=models.ForeignKey(limit_choices_to={'Choose_College__college_name': 'College of Science'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.departments'),
        ),
    ]

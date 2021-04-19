# Generated by Django 3.1.8 on 2021-04-12 20:18

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20210412_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjects',
            name='hours',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='prerequisites',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='home.Subjects'),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='units',
            field=models.IntegerField(default=1),
        ),
    ]
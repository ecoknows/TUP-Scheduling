# Generated by Django 3.1.8 on 2021-04-13 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_loginpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjects',
            name='chevy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='home.subjects'),
        ),
    ]
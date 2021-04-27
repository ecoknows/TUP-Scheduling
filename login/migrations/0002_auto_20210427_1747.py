# Generated by Django 3.1.8 on 2021-04-27 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginpage',
            name='carousel_image',
            field=models.ForeignKey(blank=True, help_text='For best fit, please choose a size of 772x667', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
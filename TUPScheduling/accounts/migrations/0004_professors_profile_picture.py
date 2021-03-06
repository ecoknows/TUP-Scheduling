# Generated by Django 3.1.8 on 2021-06-16 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('accounts', '0003_auto_20210616_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='professors',
            name='profile_picture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.image'),
        ),
    ]

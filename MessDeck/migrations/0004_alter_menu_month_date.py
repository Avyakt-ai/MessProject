# Generated by Django 4.2.7 on 2023-11-21 19:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MessDeck', '0003_remove_menu_date_time_remove_staffprofile_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='month_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-24 10:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MessDeck', '0008_rename_menu_menuitem_meal_alter_menudate_month_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menudate',
            name='month_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
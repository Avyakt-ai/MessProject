# Generated by Django 4.2.7 on 2023-11-24 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MessDeck', '0009_alter_menudate_month_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuitem',
            old_name='meal',
            new_name='menu',
        ),
    ]
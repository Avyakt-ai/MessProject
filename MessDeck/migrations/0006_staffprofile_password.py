# Generated by Django 4.2.7 on 2023-11-24 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MessDeck', '0005_alter_studentprofile_bits_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffprofile',
            name='password',
            field=models.CharField(default='123', max_length=50),
        ),
    ]

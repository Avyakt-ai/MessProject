# Generated by Django 4.2.7 on 2023-11-29 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MessDeck', '0018_alter_complaint_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MessDeck.studentprofile'),
        ),
    ]

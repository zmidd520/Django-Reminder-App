# Generated by Django 4.2.6 on 2023-11-01 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder_app', '0004_alter_reminder_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='date',
            field=models.DateField(default=None),
        ),
    ]
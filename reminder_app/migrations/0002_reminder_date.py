# Generated by Django 4.2.6 on 2023-11-01 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='date',
            field=models.DateField(default=None),
        ),
    ]
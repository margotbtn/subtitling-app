# Generated by Django 4.2.3 on 2023-07-27 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subtitlingAI', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videofile',
            name='description',
        ),
    ]

# Generated by Django 4.2.3 on 2023-07-27 15:04

from django.db import migrations, models
import subtitlingAI.validators


class Migration(migrations.Migration):

    dependencies = [
        ('subtitlingAI', '0002_remove_videofile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videofile',
            name='video_file',
            field=models.FileField(upload_to='documents/', validators=[subtitlingAI.validators.validate_file_extension]),
        ),
    ]

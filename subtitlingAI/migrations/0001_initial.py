# Generated by Django 4.2.3 on 2023-08-24 02:54

from django.db import migrations, models
import subtitlingAI.models
import subtitlingAI.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideoFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_project_id', models.CharField(default='158846036087', max_length=100, validators=[subtitlingAI.validators.validate_google_project_id])),
                ('video_file', models.FileField(upload_to=subtitlingAI.models.VideoFile.get_upload_path, validators=[subtitlingAI.validators.validate_file_extension])),
                ('transcription_language', models.CharField(choices=[('EN', 'English'), ('FR', 'French'), ('ES', 'Spanish')], default='EN', max_length=5)),
            ],
        ),
    ]

from django.db import models
from subtitlingAI.validators import validate_file_extension, validate_google_project_id

class VideoFile(models.Model):

    class Language(models.TextChoices):
        ENGLISH = 'EN'
        FRENCH = 'FR'
        SPANISH = 'ES'
    
    project_id = models.fields.CharField(default='158846036087', max_length=100, validators=[validate_google_project_id])
    video_file = models.FileField(upload_to=f'uploaded/', validators=[validate_file_extension])
    transcription_language = models.fields.CharField(choices=Language.choices, max_length=5, default='EN')

    def get_upload_path(instance, filename):
        return f'uploaded/{instance.project_id}/{filename}'
    
    video_file.upload_to = get_upload_path
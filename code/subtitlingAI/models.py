from django.db import models
from subtitlingAI.validators import validate_file_extension

class VideoFile(models.Model):
    video_file = models.FileField(upload_to='uploaded/', validators=[validate_file_extension])
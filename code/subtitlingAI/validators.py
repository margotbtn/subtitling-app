from django.core.exceptions import ValidationError
from google.cloud import resource_manager
import magic


def validate_file_extension(value):
    allowed_formats = ['video/x-matroska', 'video/avi', 'video/mp4']
    mime = magic.Magic(mime=True)
    file_mime_type = mime.from_buffer(value.read())
    
    if file_mime_type not in allowed_formats:
        raise ValidationError("Invalid video file format. Only MKV, AVI, and MP4 formats are allowed.")

def validate_google_project_id(value):
    client = resource_manager.Client()
    try:
        project = client.fetch_project(value)
        return True
    except Exception as e:
        raise ValidationError("Invalid video file format. Only MKV, AVI, and MP4 formats are allowed.")
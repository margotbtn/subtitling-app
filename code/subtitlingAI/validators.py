from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from google.cloud import resource_manager


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.avi', '.mkv', '.mp4']
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            _("Unsupported file extension."),
            code="unvalid"
        )

def validate_google_project_id(value):
    client = resource_manager.Client()
    try:
        project = client.fetch_project(id=value)
    except Exception as e:
        raise ValidationError(
            _("Unvalid Google Project ID"),
            code="unvalid"
        )
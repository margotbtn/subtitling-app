from django import forms
from subtitlingAI.models import VideoFile

class VideoFileForm(forms.ModelForm):
    class Meta:
        model = VideoFile
        fields = ('google_project_id', 'video_file', 'transcription_language')

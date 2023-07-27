from django import forms
from subtitlingAI.models import VideoFile

class VideoFileForm(forms.ModelForm):
    class Meta:
        model = VideoFile
        fields = ('video_file',)
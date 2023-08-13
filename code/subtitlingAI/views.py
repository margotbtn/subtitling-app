from django.shortcuts import render
from subtitlingAI.forms import VideoFileForm
from subtitlingAI.models import VideoFile
from subtitlingAI.data_process.transcription import main
import shutil, os


def clean_database():
    n = VideoFile.objects.count()
    if n > 0:
        db = VideoFile.objects.all()
        for i in range(n):
            db[0].delete()

def index(request):
    clean_database()
    if request.method == "POST":
        form = VideoFileForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            main(video.project_id, video.video_file.path, video.language)
            video.delete()
            shutil.rmtree(f'uploaded/{video.project_id}')
    form = VideoFileForm()
    return render(request,
                  'subtitlingAI/index.html',
                  {'form': form})

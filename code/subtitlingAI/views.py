from django.shortcuts import render, redirect
from django.contrib import messages
from subtitlingAI.forms import VideoFileForm
from subtitlingAI.models import VideoFile
from subtitlingAI.ML.data_process import main
import shutil, os


def clean_memory():
    n = VideoFile.objects.count()
    if n > 0:
        db = VideoFile.objects.all()
        for i in range(n):
            db[0].delete()
    if os.path.exists('uploaded/'):
        shutil.rmtree('uploaded/')

def home(request):
    clean_memory()
    if request.method == "POST":
        form = VideoFileForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            main(video.video_file.path)
            video.delete()
            shutil.rmtree('uploaded/')
    form = VideoFileForm()
    return render(request,
                  'subtitlingAI/home.html',
                  {'form': form})

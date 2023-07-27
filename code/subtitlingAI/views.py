from django.shortcuts import render, redirect
from django.contrib import messages
from subtitlingAI.forms import VideoFileForm
from subtitlingAI.models import VideoFile
from subtitlingAI.data_process import main
import os, shutil


def delete_temp():
        if os.path.exists('documents/'):
            shutil.rmtree('documents/')
        n = VideoFile.objects.count()
        while n > 0:
            v = VideoFile.objects.all()[0]
            v.delete()

def home(request):
    delete_temp()
    if request.method == "POST":
        form = VideoFileForm(request.POST, request.FILES)
        if form.is_valid():
            v = form.save()
            main(v.video_file.path)
            delete_temp()
    form = VideoFileForm()
    return render(request,
                  'subtitlingAI/home.html',
                  {'form': form})

from django.shortcuts import render, redirect
from django.contrib import messages
from subtitlingAI.forms import VideoFileForm
from subtitlingAI.models import VideoFile
from subtitlingAI.ML.data_process import main
import shutil


def home(request):
    if request.method == "POST":
        form = VideoFileForm(request.POST, request.FILES)
        if form.is_valid():
            v = form.save()
            main(v.video_file.path)
            v.delete()
            shutil.rmtree('documents/')
    form = VideoFileForm()
    return render(request,
                  'subtitlingAI/home.html',
                  {'form': form})

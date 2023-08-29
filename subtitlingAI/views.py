from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from subtitlingAI.forms import VideoFileForm
from subtitlingAI.models import VideoFile
from subtitlingAI.data_process.transcription import main
import shutil

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
            srt_content = main(video.google_project_id, video.video_file.path, video.transcription_language)
            video.delete()
            shutil.rmtree(f'uploaded/{video.google_project_id}')
            response = HttpResponse(srt_content, content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="sous-titres.srt"'
            return response
        else:
            messages.warning(request, "Form not valid. Are the Google Project ID and the extension format of the video correct?")
            return redirect('index')
    form = VideoFileForm()
    return render(request,
                  'subtitlingAI/index.html',
                  {'form': form})

def about(request):
    return render(request,
                  'subtitlingAI/about.html')
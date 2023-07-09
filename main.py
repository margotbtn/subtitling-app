#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Commentaires :
* Si erreur "qt.qpa.plugin: Could not find the Qt platform plugin "wayland" in "" " : taper dans le terminal
"export QT_QPA_PLATFORM=xcb".
"""


#Libraries
from moviepy.editor import VideoFileClip
import os
import torch


#Configuration
torch.set_num_threads(1)
model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad')
(get_speech_timestamps, _, read_audio, _, _) = utils


#Variables
video_file = "/home/margot/Portfolio/subtitling-app/Test/Dune Official Trailer.mp4"


#Functions
def extract_audio(video_file, audio_file):
    video = VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile(audio_file)
    video.close()

def vad(audio_file):
    wav = read_audio(audio_file, sampling_rate=16000)
    speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=16000, visualize_probs=True, return_seconds=True)
    print(speech_timestamps)    #renvoie une liste de dictionnaires (champs 'start' et 'end' : instants en secondes des plages


#Main function
def main(video_file):
    base_path = os.path.splitext(video_file)[0]
    audio_file = base_path + ".wav"
    str_file = base_path + ".str"

    extract_audio(video_file, audio_file)
    vad(audio_file)

    os.remove(audio_file)


main(video_file)
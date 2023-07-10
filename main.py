#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Commentaires :
* Si erreur "qt.qpa.plugin: Could not find the Qt platform plugin "wayland" in "" " : taper dans le terminal
"export QT_QPA_PLATFORM=xcb".
"""


#Packages
from moviepy.editor import VideoFileClip
import os
import torch
import speech_recognition as sr
import pprint


#Configurations
torch.set_num_threads(1)
model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad')
(get_speech_timestamps, _, read_audio, _, _) = utils

r = sr.Recognizer()


#Variables
video_file_movie = "/home/margot/Portfolio/subtitling-app/Test/Dune.mp4"
video_file_speech = "/home/margot/Portfolio/subtitling-app/Test/EmmaWatson.mp4"


#Functions
def extract_audio(video_file, audio_file):
    video = VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile(audio_file)
    video.close()

def vad(audio_file):
    wav = read_audio(audio_file, sampling_rate=16000)
    speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=16000, visualize_probs=True, return_seconds=True)

    if len(speech_timestamps) >= 2:
        cur, next, last = 0, 1, len(speech_timestamps)-1
        while speech_timestamps[cur]['end'] < speech_timestamps[last]['end']:
            if speech_timestamps[next]['start'] - speech_timestamps[cur]['end'] < 1:
                speech_timestamps[cur]['end'] = speech_timestamps[next]['end']
                del speech_timestamps[next]
                last -= 1
            else:
                cur += 1
                next += 1
    return speech_timestamps    #renvoie une liste de dictionnaires (champs 'start' et 'end' : instants en secondes des plages

def asr(audio_file, periods):
    file = sr.AudioFile(audio_file)
    with file as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        for i in range(len(periods)):
            offset = min(periods[i]['start'] - 0.5, 0)
            duration = periods[i]['end'] - periods[i]['start'] + 1
            audio = r.record(source, offset=offset, duration=duration)
            try:
                text = r.recognize_google(audio)    #paramètre show_all=True pour renvoyer JSON string avec toutes les possibilités
            except:
                text = None
            periods[i]['text'] = text
    pprint.pprint(periods)
    return periods


#Main function
def main(video_file):
    base_path = os.path.splitext(video_file)[0]
    audio_file = base_path + ".wav"
    str_file = base_path + ".str"

    extract_audio(video_file, audio_file)
    periods = vad(audio_file)
    asr(audio_file, periods)

    os.remove(audio_file)


main(video_file_speech)
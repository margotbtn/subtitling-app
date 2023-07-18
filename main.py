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
video_file = "/home/margot/Portfolio/subtitling-app/Test/Dune.mp4"    #Dune ou EmmaWatson



#---------------------------------------- Functions -----------------------------------------

def extract_audio(video_file, audio_file):
    video = VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile(audio_file)
    video.close()

def format_time(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

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
                text = "[ASR not working]"
            periods[i]['text'] = text
    #pprint.pprint(periods)
    return periods

def srt(subtitles, srt_file):
    srt_content = ""
    for i, sub in enumerate(subtitles, start=1):
        start = format_time(sub['start'])
        end = format_time(sub['end'])
        text = sub['text']
        srt_content += f"{i}\n{start} --> {end}\n{text}\n\n"
    with open(srt_file, 'w', encoding='utf-8') as f:
        f.write(srt_content)


#---------------------------------------- Main function -----------------------------------------

def main(video_file):
    base_path = os.path.splitext(video_file)[0]
    audio_file = base_path + ".wav"
    srt_file = base_path + ".srt"

    extract_audio(video_file, audio_file)

    print("Processing VAD.")
    periods = vad(audio_file)
    print("VAD - Done.")

    print("Processing ASR.")
    subtitles = asr(audio_file, periods)
    os.remove(audio_file)
    print("ASR - Done.")

    print("Writing in the SRT file.")
    srt(subtitles, srt_file)
    print("SRT - Done.")


main(video_file)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Commentaires :

Si erreur "qt.qpa.plugin: Could not find the Qt platform plugin "wayland" in "" " : taper dans le terminal
"export QT_QPA_PLATFORM=xcb".
"""


#Packages
from moviepy.editor import VideoFileClip
import os
import torch
from subtitlingAI.ML.asr import asr_web_speech, asr_cloud_speech    #Valeurs possibles prises par asr_function


#Configurations
torch.set_num_threads(1)
model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad')
(get_speech_timestamps, _, read_audio, _, _) = utils


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
    return speech_timestamps

def generate_subtitles(audio_file):
    periods = vad(audio_file)
    for i, period in enumerate(periods, start=1):
        period['id'] = i
        period['text'] = asr_cloud_speech(audio_file, period['start'], period['end'])
    return periods

def write_in_srt(subtitles, srt_file):
    srt_content = ""
    for subtitle in subtitles:
        id = subtitle['id']
        start = format_time(subtitle['start'])
        end = format_time(subtitle['end'])
        text = subtitle['text']
        srt_content += f"{id}\n{start} --> {end}\n{text}\n\n"
    with open(srt_file, 'w', encoding='utf-8') as f:
        f.write(srt_content)


#---------------------------------------- Main function -----------------------------------------

def main(video_file):
    audio_file = os.path.splitext(video_file)[0] + '.wav'
    srt_file = os.path.join(os.path.expanduser('~'), 'Téléchargements', os.path.splitext(os.path.basename(video_file))[0] + '.srt')

    extract_audio(video_file, audio_file)
    
    print('Generate subtitles.')
    subtitles = generate_subtitles(audio_file)
    os.remove(audio_file)
    print('Subtitles - Done.')

    print("Writing in the SRT file.")
    write_in_srt(subtitles, srt_file)
    print("SRT - Done.")
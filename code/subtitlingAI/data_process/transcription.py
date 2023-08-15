#!/usr/bin/env python
# -*- coding: utf-8 -*-


from moviepy.editor import VideoFileClip
import os

from subtitlingAI.data_process.vad import vad
from subtitlingAI.data_process.asr import asr
from subtitlingAI.data_process.translation import translation


def extract_audio(video_file_path, audio_file_path):
    video = VideoFileClip(video_file_path)
    audio = video.audio
    audio.write_audiofile(audio_file_path)
    video.close()

def format_time(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def generate_subtitles(audio_file_path, project_id):
    speech_timestamps = vad(audio_file_path)
    speech_timestamps_textadded = asr(audio_file_path, speech_timestamps, project_id)
    for i, period in enumerate(speech_timestamps_textadded, start=1):
        period['id'] = i
    return speech_timestamps_textadded

def write_in_srt(subtitles, srt_file_path):
    srt_content = ""
    for subtitle in subtitles:
        id = subtitle['id']
        start = format_time(subtitle['start'])
        end = format_time(subtitle['end'])
        text = subtitle['text']
        srt_content += f"{id}\n{start} --> {end}\n{text}\n\n"
    with open(srt_file_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)

def main(google_project_id, video_file_path, required_lang):
    audio_file_path = os.path.splitext(video_file_path)[0] + '.wav'
    srt_file_path = os.path.join(os.path.expanduser('~'), 'Téléchargements', os.path.splitext(os.path.basename(video_file_path))[0] + '.srt')

    extract_audio(video_file_path, audio_file_path)
    
    print(f'Transcription')
    subtitles = generate_subtitles(audio_file_path, google_project_id)
    print('Transcription - Done.')

    print(f'Translation in {required_lang}.')
    translated_subtitles = translation(subtitles, required_lang, google_project_id)
    print('Translation - Done.')

    print("Writing in the SRT file.")
    write_in_srt(translated_subtitles, srt_file_path)
    print("SRT - Done.")
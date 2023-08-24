#!/usr/bin/env python
# -*- coding: utf-8 -*-


from moviepy.editor import VideoFileClip
import os

from subtitlingAI.data_process.vad import vad
from subtitlingAI.data_process.asr import asr
from subtitlingAI.data_process.translation import translation


def extract_audio(video_file_path, audio_file_path):
    video = VideoFileClip(video_file_path)
    duration = video.duration
    audio = video.audio
    audio.write_audiofile(audio_file_path)
    video.close()
    return duration

def format_time(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def widen_time_intervals(intervals, duration):
    new_intervals = intervals.copy()
    n = len(intervals)

    if n>0:
        cur, next = 0, 1
        for i in range(n):
            if i < n-1:
                if new_intervals[next]['start'] - new_intervals[cur]['end'] > 1:
                    new_intervals[cur]['start'] = max(0, new_intervals[cur]['start']-0.5)
                    new_intervals[cur]['end'] = min(duration, new_intervals[cur]['end']+0.5)
                    cur += 1
                    next += 1
                else:
                    new_intervals[cur]['end'] = new_intervals[next]['end']
                    del(new_intervals[next])
            else:
                new_intervals[-1]['start'] = max(0, new_intervals[-1]['start']-0.5)
                new_intervals[-1]['end'] = min(duration, new_intervals[-1]['end']+0.5)
        
        cursor = 0
        new_intervals[cursor]['sub_intervals'] = []
        for i in range(n):
            if intervals[i]['end'] < new_intervals[cursor]['end']:
                new_intervals[cursor]['sub_intervals'].append(i)
            else:
                cursor += 1
                new_intervals[cursor]['sub_intervals'] = []

    return new_intervals

def text_distribution(intervals, new_intervals):
    for new_interval in new_intervals:
        durations = [ dict['end'] - dict['start'] for dict in new_interval['sub_intervals'] ]
        prop = [ d/max(durations) for d in durations ]
        print(durations, prop)


def generate_subtitles(audio_file_path, google_project_id):
    speech_timestamps = vad(audio_file_path)
    wide_speech_timestamps = widen_time_intervals(speech_timestamps)
    asr(audio_file_path, wide_speech_timestamps, google_project_id)
    for i, period in enumerate(wide_speech_timestamps, start=1):
        period['id'] = i
    return wide_speech_timestamps

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

    duration = extract_audio(video_file_path, audio_file_path)
    
    print(f'Transcription')
    subtitles = generate_subtitles(audio_file_path, google_project_id)
    print('Transcription - Done.')

    print(f'Translation in {required_lang}.')
    translated_subtitles = translation(subtitles, required_lang, google_project_id)
    print('Translation - Done.')

    print("Writing in the SRT file.")
    write_in_srt(translated_subtitles, srt_file_path)
    print("SRT - Done.")
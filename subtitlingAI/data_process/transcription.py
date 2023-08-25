#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Import necessary libraries
from moviepy.editor import VideoFileClip
import os
import copy

# Import functions from external modules
from subtitlingAI.data_process.vad import vad
from subtitlingAI.data_process.asr import asr
from subtitlingAI.data_process.translation import translation



def extract_audio(video_file_path: str, audio_file_path: str) -> float:
    """
    Extracts audio from a video file and saves it as a separate audio file.

    Args:
        video_file_path (str): Path to the input video file.
        audio_file_path (str): Path to save the extracted audio.

    Returns:
        float: Duration of the video in seconds.
    """
    video = VideoFileClip(video_file_path)
    duration = video.duration
    audio = video.audio
    audio.write_audiofile(audio_file_path)
    video.close()
    return duration


def format_time(seconds: float) -> str:
    """
    Formats time in seconds to HH:MM:SS,mmm format.

    Args:
        seconds (float): Time in seconds.

    Returns:
        str: Formatted time string.
    """
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def widen_time_intervals(intervals: list, duration: float) -> list:
    """
    Adjusts time intervals to make them smoother and suitable for ASR.

    Args:
        intervals (list): List of time intervals (dict with 'start' and 'end').
        duration (float): Duration of the video in seconds.

    Returns:
        list: Adjusted time intervals.
    """
    new_intervals = copy.deepcopy(intervals)
    n = len(intervals)

    if n>0:
        #Merge intervals that are closer than 2 seconds and add a margin of 1 seconds before/after
        cur, next = 0, 1
        for i in range(n):
            if i < n-1:
                if new_intervals[next]['start'] - new_intervals[cur]['end'] > 2:
                    new_intervals[cur]['start'] = max(0, new_intervals[cur]['start']-1)
                    new_intervals[cur]['end'] = min(duration, new_intervals[cur]['end']+1)
                    cur += 1
                    next += 1
                else:
                    new_intervals[cur]['end'] = new_intervals[next]['end']
                    del(new_intervals[next])
            else:
                new_intervals[-1]['start'] = max(0, new_intervals[-1]['start']-1)
                new_intervals[-1]['end'] = min(duration, new_intervals[-1]['end']+1)
        
        #Keep the indices of the original intervals contained within in a field called 'sub_intervals'
        cursor = 0
        new_intervals[cursor]['sub_intervals'] = []
        for i in range(n):
            if intervals[i]['end'] < new_intervals[cursor]['end']:
                new_intervals[cursor]['sub_intervals'].append(i)
            else:
                cursor += 1
                new_intervals[cursor]['sub_intervals'] = [i, ]

    return new_intervals


def split_text_proportionally(text: str, prop: list) -> list:
    """
    Splits text proportionally based on provided proportions.

    Args:
        text (str): Input text to be split.
        prop (list): List of proportions for splitting.

    Returns:
        list: List of split text segments.
    """
    #List of words composing the string text
    words = text.split()

    #nclude the punctuation with the words
    i = 1
    for j in range(len(words)-1):
        if words[i] in ['?', '!', ':']:
            words[i-1] += ' ' + words[i]
            del(words[i])
        else:
            i += 1

    n = len(words)
    #Number of words according to the proportions given
    distribution = [round(p*n) for p in prop]

    #List of the strings whose words numbers are given by distribution
    results = []
    for i in distribution:
        results.append(" ".join(words[:i]))
        del(words[:i])

    return results


def text_distribution(intervals: list, new_intervals: list):
    """
    Distributes text segments onto adjusted time intervals.

    Args:
        intervals (list): Original time intervals (dict with 'start' and 'end').
        new_intervals (list): Adjusted time intervals (dict with 'sub_intervals' and 'text').
    """
    for new_interval in new_intervals:
        durations = [ intervals[i]['end'] - intervals[i]['start'] for i in new_interval['sub_intervals'] ]
        prop = [ d/sum(durations) for d in durations ]
        texts = split_text_proportionally(new_interval['text'], prop)
        for i, j in zip(new_interval['sub_intervals'], range(len(texts))):
            intervals[i]['text'] = texts[j]


def generate_subtitles(audio_file_path: str, duration: float, google_project_id: str) -> list:
    """
    Generates subtitles by performing various processing steps.

    Args:
        audio_file_path (str): Path to the extracted audio file.
        duration (float): Duration of the video in seconds.
        google_project_id (str): Google Cloud project ID for ASR.

    Returns:
        list: List of generated subtitles.
    """
    speech_timestamps = vad(audio_file_path)
    wide_speech_timestamps = widen_time_intervals(speech_timestamps, duration)
    asr(audio_file_path, wide_speech_timestamps, google_project_id)
    text_distribution(speech_timestamps, wide_speech_timestamps)
    for i, period in enumerate(speech_timestamps, start=1):
        period['id'] = i
    return speech_timestamps


def write_in_srt(subtitles: list, srt_file_path: str):
    """
    Writes subtitles into an SRT file.

    Args:
        subtitles (list): List of subtitles (dict with 'id', 'start', 'end', and 'text').
        srt_file_path (str): Path to save the SRT file.
    """
    srt_content = ""
    for subtitle in subtitles:
        id = subtitle['id']
        start = format_time(subtitle['start'])
        end = format_time(subtitle['end'])
        text = subtitle['text']
        srt_content += f"{id}\n{start} --> {end}\n{text}\n\n"
    with open(srt_file_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)


def main(google_project_id: str, video_file_path: str, required_lang: str):
    """
    Main function to automate the subtitling process.

    Args:
        google_project_id (str): Google Cloud project ID for ASR and translation.
        video_file_path (str): Path to the input video file.
        required_lang (str): Desired language for translation.
    """
    audio_file_path = os.path.splitext(video_file_path)[0] + '.wav'
    srt_file_path = os.path.join(os.path.expanduser('~'), 'Téléchargements', os.path.splitext(os.path.basename(video_file_path))[0] + '.srt')

    duration = extract_audio(video_file_path, audio_file_path)
    
    print(f'Transcription')
    subtitles = generate_subtitles(audio_file_path, duration, google_project_id)
    print('Transcription - Done.')

    print(f'Translation in {required_lang}.')
    translated_subtitles = translation(subtitles, required_lang, google_project_id)
    print('Translation - Done.')

    print("Writing in the SRT file.")
    write_in_srt(translated_subtitles, srt_file_path)
    print("SRT - Done.")
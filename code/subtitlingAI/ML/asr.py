#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Commentaires :

Outils au choix pour ASR :
    - Web Speech API (web_speech)
    - Google Cloud Speech (cloud_speech)
"""


#Packages
import speech_recognition as sr
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from pydub import AudioSegment
import os


#---------------------------------------- Google Web Speech API -----------------------------------------

def asr_web_speech(audio_file, start, end):
    r = sr.Recognizer()
    file = sr.AudioFile(audio_file)
    offset = start - 0.5
    duration = end - start + 1
    with file as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.record(source, offset=offset, duration=duration)
        try:
            text = r.recognize_google(audio)    #paramètre show_all=True pour renvoyer JSON string avec toutes les possibilités
        except:
            text = '[ASR not working]'
    return text


#---------------------------------------- Google Cloud Speech -----------------------------------------

def transcribe_feature_in_recognizer(project_id: str, recognizer_id: str, audio_file: str) -> cloud_speech.RecognizeResponse:
    # Instantiates a client
    client = SpeechClient()

    # Reads a file as bytes
    with open(audio_file, "rb") as f:
        content = f.read()

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{project_id}/locations/global/recognizers/{recognizer_id}",
        content=content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    text = ""
    for result in response.results:
        try:
            text += result.alternatives[0].transcript
        except:
            pass

    return text

def cut_audio(audio_file, start, end):
    audio = AudioSegment.from_wav(audio_file)
    audio_cut = audio[(start*1000):(end*1000)]
    audio_file_cut = os.path.splitext(audio_file)[0] + '_cut.wav'
    audio_cut.export(audio_file_cut, format="wav")
    return audio_file_cut

def asr_cloud_speech(audio_file, start, end):
    if end - start > 60:
        return (asr_cloud_speech(audio_file, start, start+60) + asr_cloud_speech(audio_file, start+60, end))
    else:
        audio_file_cut = cut_audio(audio_file, start, end)
        text = transcribe_feature_in_recognizer(project_id='158846036087', recognizer_id='recognizer-en-long-punc', audio_file=audio_file_cut)
        os.remove(audio_file_cut)
        return text
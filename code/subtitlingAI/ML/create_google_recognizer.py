#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Commentaires :

Ponctuation automatique prise en charge.
"""


#Packages
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

def create_recognizer(project_id: str, recognizer_id: str) -> cloud_speech.Recognizer:
    # Instantiates a client
    client = SpeechClient()

    request = cloud_speech.CreateRecognizerRequest(
        parent=f"projects/{project_id}/locations/global",
        recognizer_id=recognizer_id,
        recognizer=cloud_speech.Recognizer(
            default_recognition_config=cloud_speech.RecognitionConfig(
                auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
                language_codes=["en-US"],
                model="long",
                features=cloud_speech.RecognitionFeatures(
                    enable_automatic_punctuation=True,
                ),
            ),
        ),
    )

    operation = client.create_recognizer(request=request)
    recognizer = operation.result()

    print("Created Recognizer:", recognizer.name)


#create_recognizer(project_id='subtitles-ai', recognizer_id='recognizer-en-long-punc')
#Created Recognizer: projects/158846036087/locations/global/recognizers/recognizer-en-long-punc
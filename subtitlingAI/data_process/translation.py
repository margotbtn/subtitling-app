#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Import necessary libraries
from google.cloud import translate



def detect_language(text: str, project_id: str) -> str:
    """
    Detects the language of a given text using the Google Cloud Translation API.

    Args:
        text (str): Text for language detection.
        project_id (str): Google Cloud project ID.

    Returns:
        str: Detected language code (e.g., "en" for English).
    """    
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.detect_language(
        content=text,
        parent=parent,
        mime_type="text/plain",
    )

    return response.languages[0].language_code


def translate_text(text: str, source_lang: str, required_lang: str, project_id: str) -> str:
    """
    Translates the given text from the source language to the required language
    using the Google Cloud Translation API.

    Args:
        text (str): Text to be translated.
        source_lang (str): Source language code (e.g., "en" for English).
        required_lang (str): Target language code for translation.
        project_id (str): Google Cloud project ID.

    Returns:
        str: Translated text in the required language.
    """
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_lang,
            "target_language_code": required_lang,
        }
    )

    print('Translated text:', response.translations[0].translated_text)
    return response.translations[0].translated_text


def translation(subtitles: list, required_lang: str, google_project_id: str) -> list:
    """
    Translates the text of each subtitle to the required language if necessary.

    Args:
        subtitles (list): List of subtitles (dict with 'id' and 'text').
        required_lang (str): Target language code for translation.
        google_project_id (str): Google Cloud project ID.

    Returns:
        list: List of translated subtitles.
    """
    for subtitle in subtitles:
        try:
            source_lang = detect_language(subtitle['text'], google_project_id)
            if required_lang.upper() != source_lang.upper():
                subtitle['text'] = translate_text(subtitle['text'], source_lang, required_lang, google_project_id)
        except:
            pass
    return subtitles
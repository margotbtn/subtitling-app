#!/usr/bin/env python
# -*- coding: utf-8 -*-


from google.cloud import translate

def detect_language(text, project_id):
    
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.detect_language(
        content=text,
        parent=parent,
        mime_type="text/plain",
    )

    return response.languages[0].language_code

def translate_text(text, source_lang, required_lang, project_id):

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

def translation(subtitles, required_lang, google_project_id):
    for subtitle in subtitles:
        try:
            source_lang = detect_language(subtitle['text'], google_project_id)
            if required_lang.upper() != source_lang.upper():
                subtitle['text'] = translate_text(subtitle['text'], source_lang, required_lang, google_project_id)
        except:
            pass
    return subtitles
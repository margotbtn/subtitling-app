#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Import necessary libraries
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from google.cloud import storage
from pydub import AudioSegment
import os



def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = None

    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )

    gcs_uri = f'gs://{bucket_name}/{destination_blob_name}'

    return gcs_uri


def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    generation_match_precondition = None

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to delete is aborted if the object's
    # generation number does not match your precondition.
    blob.reload()  # Fetch blob metadata to use in generation_match_precondition.
    generation_match_precondition = blob.generation

    blob.delete(if_generation_match=generation_match_precondition)

    print(f"Blob {blob_name} deleted.")


def transcribe_batch_gcs_input_inline_output_v2(project_id: str, gcs_uri: str,) -> str:
    """Transcribes audio from a Google Cloud Storage URI.

    Args:
        project_id: The Google Cloud project ID.
        gcs_uri: The Google Cloud Storage URI.

    Returns:
        The transcript of the RecognizeResponse.
    """
    # Instantiates a client
    client = SpeechClient()

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["en-US", "fr-FR", "es-ES"],
        model="latest_long",
        features=cloud_speech.RecognitionFeatures(
                    enable_automatic_punctuation=True,
                ),
    )

    file_metadata = cloud_speech.BatchRecognizeFileMetadata(uri=gcs_uri)

    request = cloud_speech.BatchRecognizeRequest(
        recognizer=f"projects/{project_id}/locations/global/recognizers/_",
        config=config,
        files=[file_metadata],
        recognition_output_config=cloud_speech.RecognitionOutputConfig(
            inline_response_config=cloud_speech.InlineOutputConfig(),
        ),
    )

    # Transcribes the audio into text
    operation = client.batch_recognize(request=request)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=120)

    text = ""
    for result in response.results[gcs_uri].transcript.results:
        try:
            text += result.alternatives[0].transcript
        except:
            pass

    return text


def cut_audio(audio_file: str, start: float, end: float) -> str:
    """
    Cuts a segment of audio from the input audio file.

    Args:
        audio_file (str): Path to the input audio file.
        start (float): Start time of the audio segment in seconds.
        end (float): End time of the audio segment in seconds.

    Returns:
        str: Path to the cut audio file.
    """
    audio = AudioSegment.from_wav(audio_file)
    audio_cut = audio[(start*1000):(end*1000)]
    audio_file_cut = os.path.splitext(audio_file)[0] + '_cut.wav'
    audio_cut.export(audio_file_cut, format="wav")
    return audio_file_cut


def asr(audio_file_path: str, speech_timestamps: list, google_project_id: str):
    """
    Perform ASR on each speech interval using Google Cloud Speech-to-Text API.

    Args:
        audio_file_path (str): Path to the input audio file.
        speech_timestamps (list): List of speech intervals (dict with 'start' and 'end').
        google_project_id (str): Google Cloud project ID.
    """
    bucket_name = 'subtitling-app-uploaded'

    for interval in speech_timestamps:
        audio_file_cut = cut_audio(audio_file_path, interval['start'], interval['end'])
        gcs_uri = upload_blob(bucket_name, audio_file_cut, f'{google_project_id}/{os.path.basename(audio_file_cut)}')
        text = transcribe_batch_gcs_input_inline_output_v2(google_project_id, gcs_uri)
        os.remove(audio_file_cut)
        interval['text'] = text
    delete_blob(bucket_name, f'{google_project_id}/{os.path.basename(audio_file_cut)}')
#!/usr/bin/env python
# -*- coding: utf-8 -*-



"""
Commentaires :

Si erreur "qt.qpa.plugin: Could not find the Qt platform plugin "wayland" in "" " : taper dans le terminal
"export QT_QPA_PLATFORM=xcb".
"""


# Import necessary libraries
import torch

#Configurations
torch.set_num_threads(1)
model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad')
(get_speech_timestamps, _, read_audio, _, _) = utils



def vad(audio_file_path: str) -> list:
    """
    Performs Voice Activity Detection (VAD) on an audio file to detect speech segments.

    Args:
        audio_file_path (str): Path to the input audio file.

    Returns:
        list: List of speech intervals (dict with 'start' and 'end').
    """
    wav = read_audio(audio_file_path, sampling_rate=16000)
    speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=16000, visualize_probs=True, return_seconds=True)
    return speech_timestamps
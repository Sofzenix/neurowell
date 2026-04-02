# voice_text_emotion/speech.py

import speech_recognition as sr
from voice_text_emotion.text import analyze_text_emotion

from pydub import AudioSegment
import os

def analyze_speech_emotion(audio_path):
    """
    Takes an audio file path, converts speech to text,
    and performs emotion analysis on the transcribed text.
    """

    if not audio_path:
        return {
            "error": "Audio path not provided"
        }

    try:
        # Crucial bug fix: The frontend MediaRecorder yields opaque blobs (webm/ogg).
        # speech_recognition strictly requires PCM WAV. We use pydub to convert it dynamically!
        wav_path = audio_path + "_converted.wav"
        audio = AudioSegment.from_file(audio_path)
        audio.export(wav_path, format="wav")
    except Exception as e:
        return {
            "error": f"Audio processing failed, file might be corrupted: {e}"
        }

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)

        # Speech to text (Google Web Speech API)
        transcribed_text = recognizer.recognize_google(audio_data)

        # Reuse text emotion analysis
        emotion_result = analyze_text_emotion(transcribed_text)

        return {
            "transcribed_text": transcribed_text,
            "emotion": emotion_result.get("emotion"),
            "sentiment": emotion_result.get("sentiment"),
            "confidence": emotion_result.get("confidence")
        }

    except sr.UnknownValueError:
        return {
            "error": "Could not understand the audio"
        }

    except sr.RequestError as e:
        return {
            "error": f"Speech recognition service error: {e}"
        }




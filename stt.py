import os
import sounddevice as sd
import soundfile as sf
import numpy as np
from google.cloud import speech

def check_credentials():
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS ni nastavljena. "
                        "Prosim nastavite okoljsko spremenljivko z uporabo 'export'.")

def record_audio():
    RATE = 16000
    CHANNELS = 1
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "audio.wav"

    # Snemanje
    recording = sd.rec(
        int(RECORD_SECONDS * RATE),
        samplerate=RATE,
        channels=CHANNELS,
        dtype=np.int16
    )
    sd.wait()  # Počakaj, da se snemanje konča

    # Shrani posnetek
    sf.write(WAVE_OUTPUT_FILENAME, recording, RATE)
    
    return WAVE_OUTPUT_FILENAME

def transcribe_audio_google(file_path):
    check_credentials()
    client = speech.SpeechClient()

    with open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="sl-SI",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        return result.alternatives[0].transcript
    return "Prepis ni bil uspešen."

def glasovni_vnos():
    audio_file = record_audio()
    return transcribe_audio_google(audio_file)
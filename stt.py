import os
import speech_recognition as sr
from google.cloud import speech

def check_credentials():
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS ni nastavljena. "
                        "Prosim nastavite okoljsko spremenljivko z uporabo 'export'.")

def record_audio():
    WAVE_OUTPUT_FILENAME = "audio.wav"
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        # Prilagodi za okoliški hrup
        recognizer.adjust_for_ambient_noise(source)
        # Snemaj 5 sekund
        audio = recognizer.listen(source, timeout=5)
        
    # Shrani posnetek
    with open(WAVE_OUTPUT_FILENAME, "wb") as f:
        f.write(audio.get_wav_data())
    
    return WAVE_OUTPUT_FILENAME

def transcribe_audio_google(file_path):
    check_credentials()
    client = speech.SpeechClient()

    with open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionConfig.AudioEncoding.LINEAR16
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="sl-SI",
    )

    response = client.recognize(config=config, audio=speech.RecognitionAudio(content=content))

    for result in response.results:
        return result.alternatives[0].transcript
    return "Prepis ni bil uspešen."

def glasovni_vnos():
    audio_file = record_audio()
    return transcribe_audio_google(audio_file)
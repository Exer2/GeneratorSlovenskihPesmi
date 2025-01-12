import os
import pyaudio
import wave
from google.cloud import speech

# Preveri, če je okoljska spremenljivka nastavljena
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not credentials_path:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS ni nastavljena. "
                     "Prosim nastavite okoljsko spremenljivko z uporabo 'export'.")

# Nastavitve za snemanje
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "audio.wav"

# Funkcija za snemanje zvoka
def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Snemanje se je začelo... Govorite zdaj!")
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Snemanje zaključeno.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Shranjevanje posnetka
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return WAVE_OUTPUT_FILENAME

# Funkcija za prepoznavanje govora
def transcribe_audio_google(file_path):
    # Ustvarite odjemalca
    client = speech.SpeechClient()

    # Naložite avdio datoteko
    with open(file_path, "rb") as audio_file:
        content = audio_file.read()

    # Konfiguracija za prepoznavanje govora
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="sl-SI",  # Slovenski jezik
    )

    # Pošljite zahtevo
    response = client.recognize(config=config, audio=audio)

    # Izpišite prepis
    for result in response.results:
        return result.alternatives[0].transcript
    return "Prepis ni bil uspešen."

# Glavna funkcija za snemanje in prepis
def glasovni_vnos():
    audio_file = record_audio()
    return transcribe_audio_google(audio_file)

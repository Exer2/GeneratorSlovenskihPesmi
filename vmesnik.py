import streamlit as st
from generator import generator_pesmi
import os
import wave
import pyaudio
from google.cloud import speech
import streamlit as st
from generator import generator_pesmi
from dotenv import load_dotenv


# Uporabniški vmesnik V1

# Funkcija za generiranje pesmi
def generate_poem(word):
    pesem = generator_pesmi(word)
    return pesem


st.title("Pesmopisec")
word = st.text_input("Vpišite ključno besedo:")



if st.button("Generiraj pesem"):
    if word:
        poem = generate_poem(word)
        st.text_area("Vaša pesem:", poem, height=500)       
    else:
        st.error("Vnesite ključno besedo!")


# Uporabniški vmesnik V2

# Naloži okoljske nastavitve (API ključ iz .env datoteke)
load_dotenv()
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not credentials_path:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS ni nastavljena. "
                     "Prosim nastavite okoljsko spremenljivko z uporabo 'export'.")


def record_audio():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "audio.wav"

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    st.write("Snemanje se je začelo... Govorite zdaj!")
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    st.write("Snemanje zaključeno.")
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


if st.button("Posnemi in generiraj pesem"):
    # Snemanje govora
    audio_file = record_audio()
    st.write("Zvok je bil posnet, pretvarjam v besedilo...")

    try:
        transcript = transcribe_audio_google(audio_file)
        st.write("Prepis besedila: ", transcript)
        
        # Generiraj pesem z uporabo prepisane besede
        if transcript:
            poem = generate_poem(transcript)
            st.text_area("Vaša pesem:", poem, height=500)
        else:
            st.error("Prepis ni bil uspešen.")
    except Exception as e:
        st.error(f"Napaka pri prepoznavanju govora: {e}")
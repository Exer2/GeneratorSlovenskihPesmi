from google.cloud import speech
from google.oauth2 import service_account
import streamlit as st
import pyaudio
import wave

# Funkcija za pridobitev poverilnic iz Streamlit Secrets
def get_google_credentials():
    credentials_json = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]
    return service_account.Credentials.from_service_account_info(credentials_json)

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

# Funkcija za prepoznavanje govora
def transcribe_audio_google(file_path):
    # Pridobitev poverilnic
    credentials = get_google_credentials()
    client = speech.SpeechClient(credentials=credentials)

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

# Streamlit UI
st.title("Pretvorba govora v besedilo")
st.write("Uporabite gumb spodaj za snemanje govora in pretvorbo v besedilo.")

if st.button("Posnemi govor"):
    record_audio()
    st.write("Zvok je posnet. Pretvarjam v besedilo...")
    try:
        transcript = transcribe_audio_google(WAVE_OUTPUT_FILENAME)
        st.write("Prepis: ", transcript)
    except Exception as e:
        st.write("Napaka pri pretvorbi: ", e)

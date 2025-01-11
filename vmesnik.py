import streamlit as st
from generator import generator_pesmi
import os




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


def get_google_credentials():
    credentials_json = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]
    return service_account.Credentials.from_service_account_info(credentials_json)

def record_audio():
    RATE = 16000  # Sampling rate
    CHANNELS = 1  # Mono audio
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "audio.wav"

    st.write("Snemanje se je začelo... Govorite zdaj!")
    
    # Record audio
    audio_data = sd.rec(int(RATE * RECORD_SECONDS), samplerate=RATE, channels=CHANNELS, dtype='int16')
    sd.wait()  # Wait until recording is finished
    st.write("Snemanje zaključeno.")
    
    # Save audio to file
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit audio corresponds to 2 bytes
        wf.setframerate(RATE)
        wf.writeframes(audio_data.tobytes())
    
    return WAVE_OUTPUT_FILENAME

# Funkcija za prepoznavanje govora
def transcribe_audio_google(file_path):
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

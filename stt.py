import pyaudio
import wave
import os
from google.cloud import speech
import streamlit as st

# Nastavitve za snemanje
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# Funkcija za snemanje
def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    frames = []

    st.write("Recording...")

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    st.write("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Funkcija za pretvorbo govora v besedilo
def transcribe_audio():
    client = speech.SpeechClient()
    with open(WAVE_OUTPUT_FILENAME, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        return result.alternatives[0].transcript

# Uporabniški vmesnik z uporabo Streamlit
def main():
    st.title("Speech to Text App")
    if st.button("Start Recording"):
        record_audio()
        text = transcribe_audio()
        st.write("Transcribed text: ", text)
        with open("vmesnik.py", "w") as file:
            file.write("Transcribed text: " + text)

if __name__ == "__main__":
    main()

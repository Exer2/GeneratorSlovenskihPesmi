import os
import streamlit as st
from google.cloud import speech
import pyaudio
from six.moves import queue
import json

# Audio snemalna konfiguracija
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class MicrophoneStream:
    """Zajema zvok z mikrofona in ga strežnikom posreduje v delih."""
    def __init__(self, rate, chunk):
        self.rate = rate
        self.chunk = chunk
        self.buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self.audio_interface = pyaudio.PyAudio()
        self.audio_stream = self.audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
            stream_callback=self._fill_buffer,
        )
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.closed = True
        self.buff.put(None)
        self.audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Shranjuje zvok v predpomnilnik."""
        self.buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """Generator, ki strežniku posreduje zvočne podatke."""
        while not self.closed:
            chunk = self.buff.get()
            if chunk is None:
                return
            yield chunk

def record_audio():
    """Zajame govor in vrne prepoznano besedilo."""
    # Pridobi poverilnice iz Streamlit Secrets
    google_creds = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]["credentials_json"]

    # Ustvari začasno datoteko za poverilnice
    with open("temp_google_credentials.json", "w") as temp_file:
        temp_file.write(google_creds)

    # Nastavi pot do poverilnic
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "temp_google_credentials.json"

    client = speech.SpeechClient()

    # Konfiguracija za Google Cloud Speech API
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="sl-SI",  # Spremenite v ustrezen jezik (npr. "en-US" za angleščino)
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=False,  # Vrnemo samo dokončne rezultate
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_generator)
        responses = client.streaming_recognize(streaming_config, requests)

        try:
            for response in responses:
                for result in response.results:
                    if result.is_final:
                        return result.alternatives[0].transcript
        finally:
            # Počisti začasno datoteko
            os.remove("temp_google_credentials.json")

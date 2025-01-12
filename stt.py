import pyaudio
import queue
import os
from google.cloud import speech

def record_audio():
    """Funkcija za zajemanje zvoka in prepoznavanje govora z Google Cloud Speech-to-Text."""
    # Nastavitve za PyAudio
    RATE = 16000
    CHUNK = int(RATE / 10)  # 100ms okvirji
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    # Ustvarimo vrsto za shranjevanje zajetega zvoka
    audio_queue = queue.Queue()

    def callback(in_data, frame_count, time_info, status):
        """Callback funkcija za PyAudio."""
        audio_queue.put(in_data)
        return None, pyaudio.paContinue

    # Nastavimo Google Cloud Speech klienta
    client = speech.SpeechClient()

    # Nastavitve za prepoznavanje
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="sl-SI",
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=False,
    )

    # Začnemo s PyAudio streamom
    audio_interface = pyaudio.PyAudio()
    stream = audio_interface.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        stream_callback=callback,
    )

    # Funkcija za pošiljanje avdio podatkov Google API-ju
    def generate_audio():
        while True:
            chunk = audio_queue.get()
            if chunk is None:
                break
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    # Zagon Google Cloud Speech prepoznavanja
    responses = client.streaming_recognize(
        config=streaming_config,
        requests=generate_audio()
    )

    try:
        print("Začnite govoriti...")
        for response in responses:
            for result in response.results:
                if result.is_final:
                    text = result.alternatives[0].transcript
                    print(f"Prepoznano besedilo: {text}")
                    # Posredujemo besedilo v datoteko `vmesnik.py`
                    with open("recognized_text.txt", "w") as file:
                        file.write(text)
                    return  # Zaključimo po prvi prepoznani besedi
    finally:
        # Počistimo in zapremo stream
        stream.stop_stream()
        stream.close()
        audio_interface.terminate()

if __name__ == "__main__":
    record_audio()
from huggingface_hub import InferenceClient
#from config import API_KEY
import os
import requests

from langdetect import detect


API_KEY = os.getenv("API_KEY")
PLAYHT_API_KEY = os.getenv("PLAYHT_API_KEY")
PLAYHT_USER_ID = os.getenv("PLAYHT_USER_ID")



def preveri_jezik(stavek):
    return detect(stavek) == "sl"

def odstrani_neslovenske_besede(besedilo):
    vrstice = besedilo.split("\n")
    filtrirane_vrstice = []
    for vrstica in vrstice:
        besede = vrstica.split()
        filtrirane_besede = [beseda for beseda in besede if preveri_jezik(beseda)]
        filtrirane_vrstice.append(" ".join(filtrirane_besede))
    return "\n".join(filtrirane_vrstice)


def generator_pesmi(kljucna_beseda):
    client = InferenceClient(api_key=API_KEY)
    messages = [
	    { "role": "user", "content": f"Napiši pesem v slovenščini s pomočjo ključne besede: {kljucna_beseda}. Napiši le pesem z naslovom. Pesem naj ima najmanj 1 in največ 4 kitice" }
    ]
    stream = client.chat.completions.create(
        model="Qwen/Qwen2.5-72B-Instruct", 
        messages=messages, 
        temperature=0.9,
        top_p=0.9,
        max_tokens=1000,
        stream=True
    )
    pesem = ""

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:  # Preverimo, ali je del besedila prazen
            pesem += content

    return pesem



PLAYHT_API_KEY = os.getenv("PLAYHT_API_KEY")
PLAYHT_USER_ID = os.getenv("PLAYHT_USER_ID")  # Vaša PlayHT uporabniška ID

def text_to_speech(text, voice="Petra"):
    url = "https://play.ht/api/v1/convert"
    headers = {
        "Authorization": f"Bearer {PLAYHT_API_KEY}",
        "X-User-ID": PLAYHT_USER_ID,
        "Content-Type": "application/json",
    }
    data = {
        "content": [text],  # PlayHT sprejme besedilo kot seznam vrstic
        "voice": voice,  # Nastavite glas, npr. "Maja" za slovenščino
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        audio_url = response.json().get("audio_url")
        return audio_url
    else:
        raise Exception(f"Napaka pri generiranju TTS: {response.json()}")

# Testiranje:
# audio_url = text_to_speech("To je test besedila.")
# print(audio_url)

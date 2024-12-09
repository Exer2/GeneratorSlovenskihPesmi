from huggingface_hub import InferenceClient
#from config import API_KEY
import os

from langdetect import detect


API_KEY = os.getenv("API_KEY")



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

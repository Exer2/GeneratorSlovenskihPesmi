from huggingface_hub import InferenceClient
#from config import API_KEY
import os

API_KEY = os.getenv("API_KEY")

def generator_pesmi(kljucna_beseda):
    client = InferenceClient(api_key=API_KEY)
    messages = [
	    { "role": "user", "content": f"Ali lahko napišeš pesem v slovenščini s pomočjo ključne besede: {kljucna_beseda}? Napiši le pesem, brez začetnega stavka." },
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

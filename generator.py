import os
from huggingface_hub import InferenceClient

# API ključ, pridobljen iz okoljske spremenljivke
"""
API_KEY = os.getenv("API_KEY")

def generator_pesmi(kljucna_beseda):
    # Ustvarimo stranko za poizvedbe
    client = InferenceClient(api_key=API_KEY)
    
    # Navodila za model
    prompt = f"Napiši pesem v slovenščini glede na ključno besedo: {kljucna_beseda}. Izpiši samo naslov in pod naslovom samo pesem."
    
    # Zahteva za generacijo odgovora
    response = client.text_generation(
        model="utter-project/EuroLLM-9B-Instruct", 
        inputs=prompt,
        parameters={
            "temperature": 0.9,  # Kreativnost
            "top_p": 0.9,        # Verjetnostne kombinacije
            "max_new_tokens": 1000  # Največje število generiranih tokenov
        }
    )

    
    
    # Pridobimo generirano pesem iz odgovora
    pesem = response.get("generated_text", "")
    
    return pesem
    """


from transformers import pipeline

# Ustvarimo pipeline za generacijo besedila
pipe = pipeline("text-generation", model="utter-project/EuroLLM-9B-Instruct")

def generator_pesmi(kljucna_beseda):
    # Priprava sporočila (prompt) za model
    prompt = f"Napiši pesem v slovenščini glede na ključno besedo: {kljucna_beseda}. Izpiši samo naslov in pod naslovom samo pesem."

    # Generacija besedila z uporabo pipeline
    result = pipe(prompt, max_length=200, temperature=0.9, top_p=0.9, num_return_sequences=1)
    
    # Pridobitev generiranega besedila iz odgovora
    pesem = result[0]["generated_text"]
    return pesem
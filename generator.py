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
from transformers import AutoModelForCausalLM, AutoTokenizer

# Določite ID modela
model_id = "utter-project/EuroLLM-9B-Instruct"

# Nalaganje modela in tokenizerja
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

def generator_pesmi(kljucna_beseda):
    """
    Funkcija generira pesem glede na podano ključno besedo.
    
    Args:
        kljucna_beseda (str): Ključna beseda, na podlagi katere se generira pesem.

    Returns:
        str: Generirana pesem.
    """
    # Definirajte sporočilo za model
    messages = [
        {
            "role": "system",
            "content": "You are EuroLLM --- an AI assistant specialized in European languages that provides safe, educational and helpful answers.",
        },
        {
            "role": "user", 
            "content": f"Napiši pesem v slovenščini glede na ključno besedo: {kljucna_beseda}. Izpiši samo naslov in pod naslovom samo pesem."
        },
    ]

    # Priprava vhodnih podatkov za model
    inputs = tokenizer.apply_chat_template(
        messages, 
        tokenize=True, 
        add_generation_prompt=True, 
        return_tensors="pt"
    )

    # Generacija pesmi
    outputs = model.generate(inputs["input_ids"], max_new_tokens=1024, temperature=0.9, top_p=0.9)

    # Dekodiranje in vrnitev generirane pesmi
    pesem = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return pesem
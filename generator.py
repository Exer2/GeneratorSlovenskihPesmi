from huggingface_hub import InferenceClient
import os


API_KEY = os.getenv("API_KEY")

def generator_pesmi(kljucna_beseda):
    client = InferenceClient(api_key=API_KEY)
    messages = [
	    { "role": "user", "content": f"Napiši pesem v slovenščini glede na ključno besedo: {kljucna_beseda}. Izpiši samo naslov in pod naslovom samo pesem." }
    ]
    stream = client.chat.completions.create(
        model="utter-project/EuroLLM-1.7B-Instruct", 
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




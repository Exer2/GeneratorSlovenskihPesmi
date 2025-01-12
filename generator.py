import os
import google.generativeai

API_KEY = os.getenv("API_KEY")
google.generativeai.configure(api_key=API_KEY)

def generator_pesmi(kljucna_beseda):
    model = google.generativeai.GenerativeModel("gemini-1.5-flash-8b")
    response = model.generate_content(f"Napiši kratko pesem v slovenščini glede na ključno besedo: {kljucna_beseda}. Poskusi uporabiti najboljše rime, kot jih lahko.")
    return response.text
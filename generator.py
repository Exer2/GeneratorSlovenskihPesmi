import os
import google.generativeai

API_KEY = os.getenv("API_KEY")
google.generativeai.configure(api_key=API_KEY)

def generator_pesmi(kljucna_beseda):
    model = google.generativeai.GenerativeModel("gemini-2.0-flash-exp")
    response = model.generate_content(f"Prevzami vlogo pesnika, pisatelja pesmi. Napiši kratko pesem v slovenščini glede na ključno besedo: {kljucna_beseda}. Uporabljaj rime, kot jih slovenski pesniki uporabljajo v svojih pesmih, kot na primer verižna rima, zaporedna rima, končna rima, prestopna rima itd.")
    return response.text
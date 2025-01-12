from huggingface_hub import InferenceClient
import os
import google.generativeai

API_KEY = os.getenv("API_KEY")
google.generativeai.configure(api_key=API_KEY)

"""def generator_pesmi(kljucna_beseda):
    client = InferenceClient(api_key=API_KEY)
    messages = [
	    { "role": "user", "content": f"Napiši pesem v slovenščini s pomočjo ključne besede: {kljucna_beseda}. Izpiši le naslov in pod naslovom le pesem." }
    ]
    stream = client.chat.completions.create(
        model="Qwen/Qwen2.5-72B-Instruct", 
        messages=messages, 
        temperature=0.9,
        top_p=0.9,
        max_tokens=200,
        stream=True
    )

    pesem = ""

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:  # Preverimo, ali je del besedila prazen
            pesem += content

    return pesem
    """
    def generator_pesmi(kljucna_beseda):
        

        model = google.generativeai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Explain how AI works")
        return response.text
import os
import google.generativeai

API_KEY = os.getenv("API_KEY")
google.generativeai.configure(api_key=API_KEY)

def generator_pesmi(kljucna_beseda):
    model = google.generativeai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"""Ustvari pesem na podlagi ključne besede: {kljucna_beseda}. 
        Tvoj odgovor naj vsebuje naslov pesmi in celotno besedilo pesmi. 
        Oblikuj pesem tako, da ima jasno strukturo, kot so kitice in morebiten refren. 
        Naj bo odgovor predstavljen v obliki:
        Naslov pesmi
        (brez narekovajev ali dodatnih uvodnih besed)
        Nova vrstica
        Besedilo pesmi (razdeljeno na kitice ali refrene, če je primerno)

        Primer strukture:

        Lorem ipsum

        Lorem ipsum dolor sit amet, 
        consectetur adipiscing elit. 
        Fusce ante nisi, tempus a elementum vel, 
        gravida et nulla. 

        Maecenas maximus mi 
        et lorem euismod placerat. 
        Aliquam non faucibus sapien. 
        Donec fringilla semper 
        nibh ac volutpat. Sed iaculis, 
        nisl vel cursus sodales. 

        odio mauris sagittis ex, 
        ut dictum lectus leo eu elit. 
        Nam eget elit vel augue congue condimentum. 
        Maecenas feugiat ligula 
        bibendum aliquam faucibus. 

        Na ključni besedi se osredotoči kot na osrednjo temo pesmi, 
        vendar jo uporabi nežno in umetniško. Poskusi z vključevanjem čustev, 
        uporabo znanih struktur rim v slovenskih pesmih in glasbenega ritma. 
        Na koncu odgovora ne dodajaj dodatnih razlag ali uvodov – preprosto samo pesem."""
    )
    return response.text
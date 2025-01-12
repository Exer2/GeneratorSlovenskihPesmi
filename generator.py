import os
import google.generativeai

API_KEY = os.getenv("API_KEY")
google.generativeai.configure(api_key=API_KEY)

def generator_pesmi(kljucna_beseda):
    model = google.generativeai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"""Ustvari pesem v slovenskem knjižnem jeziku na podlagi ključne besede: {kljucna_beseda}.

            Tvoj odgovor naj vsebuje:

            *   Naslov pesmi: Izberi naslov, ki je tematsko povezan s ključno besedo in odraža vzdušje pesmi.
            *   Celotno besedilo pesmi: Pesem naj bo napisana v knjižnem slovenskem jeziku, z uporabo bogatega besedišča in smiselno povezanih besed.
            *   Jasno strukturo: Pesem naj ima jasno razvidne kitice in morebiten refren, ki se ponavlja in poudarja osrednjo temo.
            *   Rime in ritem: Uporabi tradicionalne slovenske rime (npr. ABAB, AABB, ABCB) in ustvari melodičen ritem, ki spominja na uveljavljene slovenske pesmi. Izogibaj se prisiljenim rimam in poskrbi, da se besede naravno ujemajo.
            *   Čustva in metafore: Vključi čustva, ki jih vzbuja ključna beseda, in uporabi metafore ali druge pesniške figure, da obogatiš izraznost pesmi.
            *   Osredotočenost na ključno besedo: Ključna beseda naj bo osrednja tema pesmi, vendar jo uporabi nežno in umetniško, ne preveč očitno ali ponavljajoče.

            Oblika odgovora naj bo naslednja:

            Naslov pesmi
            (brez narekovajev ali dodatnih uvodnih besed)

            Besedilo pesmi (razdeljeno na kitice in refrene, če obstajajo)

            Primer (za lažjo predstavo oblike):

            Naslov pesmi

            Prva kitica

            Druga kitica

            tretja kitica

            Na koncu odgovora ne dodajaj dodatnih razlag ali uvodov – preprosto samo pesem."""
    )
    return response.text
import streamlit as st
from generator import generator_pesmi

# Funkcija za generiranje pesmi
def generate_poem(word):
    pesem = generator_pesmi(word)
    return pesem

# Uporabniški vmesnik
st.title("Pesmopisec")
word = st.text_input("Vpišite ključno besedo:")



if st.button("Generiraj pesem"):
    if word:
        poem = generate_poem(word)
        st.text_area("Vaša pesem:", poem, height=500)
         # Generiraj TTS
        try:
            audio_url = text_to_speech(poem)
            st.audio(audio_url, format="audio/mp3")  # Dodaj predvajalnik
        except Exception as e:
            st.error(f"Napaka pri generiranju govora: {e}")
    else:
        st.error("Vnesite ključno besedo!")
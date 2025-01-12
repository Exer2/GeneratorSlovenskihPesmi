import streamlit as st
from generator import generator_pesmi

# Funkcija za generiranje pesmi
def generate_poem(word):
    pesem = generator_pesmi(word)
    return pesem

st.title("Pesmopisec")

# Postavimo polje za vnos in gumb v isti vrstici
col1, col2 = st.columns([4, 1])  # Določimo širino stolpcev (4:1)

with col1:
    word = st.text_input()

with col2:
    if st.button("Gumb"):
        st.info("Pritisnili ste gumb!")

if st.button("Generiraj pesem"):
    if word:
        poem = generate_poem(word)
        st.text_area("Vaša pesem:", poem, height=500)
    else:
        st.error("Vnesite ključno besedo!")
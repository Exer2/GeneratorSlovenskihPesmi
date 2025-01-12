import streamlit as st
from generator import generator_pesmi

# Funkcija za generiranje pesmi
def generate_poem(word):
    pesem = generator_pesmi(word)
    return pesem

st.title("Pesmopisec")

# Uporabimo `columns` za postavitev v isto vrstico
col1, col2 = st.columns([10, 2])  # Prilagodimo razmerje širine stolpcev

with col1:
    word = st.text_input("Vpišite ključno besedo:", label_visibility="collapsed")  # Skrijemo privzeto oznako

with col2:
    if st.button("Gumb"):
        st.info("Pritisnili ste gumb!")

if st.button("Generiraj pesem"):
    if word:
        poem = generate_poem(word)
        st.text_area("Vaša pesem:", poem, height=500)
    else:
        st.error("Vnesite ključno besedo!")
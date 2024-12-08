import streamlit as st
from generator import generator_pesmi


# Inicializacija stanja za prikaz gumba in rezultat pesmi
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False

if "poem" not in st.session_state:
    st.session_state.poem = ""


# Funkcija za generiranje pesmi
def generate_poem(word):
    st.session_state.is_generating = True  # Nastavimo stanje generiranja
    with st.spinner("Generiram pesem..."):
        pesem = generator_pesmi(word)
        st.session_state.is_generating = False  # Generiranje zaključeno
        st.session_state.poem = pesem  # Shranimo generirano pesem


# Uporabniški vmesnik
st.title("Pesmopisec")
word = st.text_input("Vpišite ključno besedo:")

# Prikaz gumba za generiranje le, če trenutno ni v stanju generiranja
if not st.session_state.is_generating:
    if st.button("Generiraj pesem"):
        if word:
            generate_poem(word)
        else:
            st.error("Vnesite ključno besedo!")

# Prikaz generirane pesmi, če obstaja
if st.session_state.poem:
    st.text_area("Vaša pesem:", st.session_state.poem, height=500)

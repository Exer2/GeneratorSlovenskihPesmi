import streamlit as st
from generator import generator_pesmi


def generate_poem(word):
    pesem = generator_pesmi(word)
    return pesem

st.title("Pesmopisec")


col1, col2 = st.columns([3, 1])

word = st.text_input("bla", 
        label_visibility="collapsed", 
        placeholder="Vnesite ključno besedo...")


# Gumb za generiranje pesmi
if st.button("Generiraj pesem"):
    if word:
        poem = generate_poem(word)
        st.text_area("Vaša pesem:", poem, height=500)
    else:
        st.error("Vnesite ključno besedo!")


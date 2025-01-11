import streamlit as st
from generator import generator_pesmi
import os




# Uporabniški vmesnik V1

# Funkcija za generiranje pesmi
def generate_poem(word):
    pesem = generator_pesmi(word)
    return pesem


st.title("Pesmopisec")
word = st.text_input("Vpišite ključno besedo:")



if st.button("Generiraj pesem"):
    if word:
        poem = generate_poem(word)
        st.text_area("Vaša pesem:", poem, height=500)       
    else:
        st.error("Vnesite ključno besedo!")


# Uporabniški vmesnik V2

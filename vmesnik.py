import streamlit as st
from generator import generator_pesmi


# Inicializacija stanja za prikaz gumba
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False


# Funkcija za generiranje pesmi
def generate_poem(word):
    pesem = generator_pesmi(word)
    return pesem


# Uporabniški vmesnik
st.title("Generator slovenskih pesmi")
word = st.text_input("Vpišite ključno besedo:")


if not st.session_state.is_generating:
    if st.button("Generiraj pesem"):
        if word:
            with st.spinner("Generiram pesem..."):
                poem = generate_poem(word)
                st.text_area("Vaša pesem:", poem, height=500)
        else:
            st.error("Vnesite ključno besedo!")



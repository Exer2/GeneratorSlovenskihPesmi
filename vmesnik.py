import streamlit as st
from gerapi import generator_pesmi

# Funkcija za generiranje pesmi
def generate_poem(word):
    pesem = generator_pesmi(word)
    return pesem

# Uporabniški vmesnik
st.title("Generator slovenskih pesmi")
word = st.text_input("Vpišite ključno besedo:")

st.markdown(
    """
    <style>
    .textarea {
        border: 2px solid black;
        border-radius: 4px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.button("Generiraj pesem"):
    if word:
        poem = generate_poem(word)
        st.text_area("Vaša pesem:", poem, height=500)
    else:
        st.error("Vnesite ključno besedo!")



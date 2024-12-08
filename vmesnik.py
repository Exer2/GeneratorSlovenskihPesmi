import streamlit as st
from generator import generator_pesmi


# Inicializacija stanja za generiranje in pesem
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False  # Ali trenutno generiramo pesem

if "poem" not in st.session_state:
    st.session_state.poem = ""  # Shrani generirano pesem


# Funkcija za generiranje pesmi
def generate_poem(word):
    st.session_state.is_generating = True  # Začetek generiranja
    try:
        with st.spinner("Generiram pesem..."):
            pesem = generator_pesmi(word)  # Klic funkcije za generacijo
        st.session_state.poem = pesem  # Shrani generirano pesem
    finally:
        st.session_state.is_generating = False  # Zaključek generiranja


# Uporabniški vmesnik
st.title("Generator slovenskih pesmi")
word = st.text_input("Vpišite ključno besedo:")

# Prikaz gumba le, če trenutno ne generiramo
if not st.session_state.is_generating:
    generate_button = st.button("Generiraj pesem")
    if generate_button:
        if word:
            generate_poem(word)
        else:
            st.error("Vnesite ključno besedo!")
else:
    st.write("Pesem se generira...")  # Prikaz stanja med generiranjem

# Prikaz generirane pesmi, če obstaja
if st.session_state.poem:
    st.text_area("Vaša pesem:", st.session_state.poem, height=500)

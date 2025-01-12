import streamlit as st
from generator import generator_pesmi

# Funkcija za generiranje pesmi
def generate_poem(word):
    pesem = generator_pesmi(word)
    return pesem

st.title("Pesmopisec")
#st.write("Vpišite ključno besedo:")

# Uporabimo `columns` za postavitev v isto vrstico
col1, col2 = st.columns([3, 1])  # Prilagodimo razmerje širine stolpcev

with col1:
    word = st.text_input("bla", label_visibility="collapsed", placeholder="Vnesite ključno besedo...")  # Skrijemo privzeto oznako

with col2:
    st.markdown("""
    <style>
    .icon-button {
        background-color: #f0f0f0;
        border: none;
        cursor: pointer;
        padding: 8px 16px;
        border-radius: 4px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    .icon-button img {
        width: 24px;
        height: 24px;
    }
    </style>
    <button class="icon-button" onclick="window.alert('Pritisnili ste ikono gumba!')">
        <img src="https://pics.freeicons.io/uploads/icons/png/3536210891586786419-512.png" alt="Ikona">
    </button>
    """, unsafe_allow_html=True)

if st.button("Generiraj pesem"):
    if word:
        poem = generate_poem(word)
        st.text_area("Vaša pesem:", poem, height=500)
    else:
        st.error("Vnesite ključno besedo!")
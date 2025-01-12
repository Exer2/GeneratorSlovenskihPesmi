import streamlit as st
from streamlit.components.v1 import html
from generator import generator_pesmi

# Funkcija za generiranje pesmi
def generate_poem(word):
    pesem = generator_pesmi(word)
    return pesem

st.title("Pesmopisec")

# Postavitev z napisom in poljem za vnos
#st.write("Vpišite ključno besedo:")
col1, col2 = st.columns([3, 1], gap="small")

with col1:
    word = st.text_input("bla", label_visibility="collapsed", placeholder="Vnesite ključno besedo...")

with col2:
    # Uporaba HTML za SVG gumb
    html("""
    <style>
    .icon-button {
        background-color: #f0f0f0;
        border: none;
        cursor: pointer;
        padding: 8px;
        border-radius: 10px;
        display: inline-flex;
        align-items: center; /* Poravnava navpično */
        justify-content: center; /* Poravnava vodoravno */
        width: 40px;
        height: 40px; /* Višina gumba nastavljena na 40px */
        margin-top: -10px; /* Poravnava glede na vnosno polje */
    }
    .icon-button svg {
        width: 24px;
        height: 24px;
        fill: #6c757d; /* Barva ikone */
    }
    .icon-button:hover svg {
        fill: #007bff; /* Barva ikone ob premiku miške */
    }
    </style>
    <button class="icon-button" onclick="alert('Pritisnili ste ikono gumba!')">
        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 16 16" style="enable-background:new 0 0 16 16;" xml:space="preserve">
            <path d="M8,11c1.657,0,3-1.343,3-3V3c0-1.657-1.343-3-3-3S5,1.343,5,3v5C5,9.657,6.343,11,8,11z"></path>
            <path d="M13,8V6h-1l0,1.844c0,1.92-1.282,3.688-3.164,4.071C6.266,12.438,4,10.479,4,8V6H3v2c0,2.414,1.721,4.434,4,4.899V15H5v1h6
    v-1H9v-2.101C11.279,12.434,13,10.414,13,8z"></path>
        </svg>
    </button>
    """, height=50)

if st.button("Generiraj pesem"):
    if word:
        poem = generate_poem(word)
        st.text_area("Vaša pesem:", poem, height=500)
    else:
        st.error("Vnesite ključno besedo!")

import streamlit as st
from generator import generator_pesmi



# Začnite z vključitvijo Font Awesome
st.markdown(
    """
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    """, unsafe_allow_html=True
)

# Funkcija za generiranje pesmi
def generate_poem(word):
    # Tu boš vključil logiko za generiranje pesmi
    pesem = generator_pesmi(word)
    return pesem

# Nastavitve za Streamlit
st.title("Pesmopisec")
word = st.text_input("Vpišite ključno besedo:")

# Gumb z ikono
if st.button("🔴 Generiraj pesem"):  # Ikona rdeče krogle za snemanje
    if word:
        poem = generate_poem(word)
        st.text_area("Vaša pesem:", poem, height=500)       
    else:
        st.error("Vnesite ključno besedo!")


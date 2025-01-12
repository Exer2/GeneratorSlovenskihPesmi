import streamlit as st
from generator import generator_pesmi



# Uporabniški vmesnik V1

# Funkcija za generiranje pesmi
def generate_poem(word):
    pesem = generator_pesmi(word)
    return pesem
    
st.title("Pesmopisec")

navodila = "Vpišite ključno besedo:"

with st.form('chat_input_form'):
    # Create two columns; adjust the ratio to your liking
    col1, col2 = st.columns([3,1]) 

    # Use the first column for text input
    with col1:
        k_beseda = st.text_input(
            navodila,
            value=navodila
            )
    with col2:
        posnemi_zvok = st.form_submit_button('Snemaj')
    
    if k_beseda and posnemi_zvok:
        # Do something with the inputted text here
        st.write(f"You said: {k_beseda}")


if st.button("Generiraj pesem"):
    if k_beseda:
        poem = generate_poem(k_beseda)
        st.text_area("Vaša pesem:", poem, height=500)       
    else:
        st.error("Vnesite ključno besedo!")
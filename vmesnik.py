import streamlit as st
from generator import generator_pesmi

# Funkcija za generiranje pesmi
def generate_poem(word):
    pesem = generator_pesmi(word)
    return pesem

# Uporabniški vmesnik
st.title("Generator slovenskih pesmi")
word = st.text_input("Vpišite ključno besedo:")



if st.button("Generiraj pesem"):
    if word:
        poem = generate_poem(word)

        lines = poem.split("\n")
        title = lines[0].strip() if lines else ""  # Prva vrstica je naslov
        body = "\n".join(lines[1:]).strip()  # Preostale vrstice so telo pesmi
        full_poem = f"**{title}**\n\n{body}"  # Združimo naslov in telo
        
        # Prikaz s krepko označenim naslovom
        st.markdown(f"**{title}**")  # Prikaz naslova krepko
        st.text_area("Vaša pesem:", poem, height=500)
    else:
        st.error("Vnesite ključno besedo!")



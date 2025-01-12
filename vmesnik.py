import streamlit as st
from generator import generator_pesmi

st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"/>',
    unsafe_allow_html=True,
)


with stylable_container(
    key="container_with_border",
    css_styles=r"""
        button p:before {
            font-family: 'Font Awesome 5 Free';
            content: '\f1c1';
            display: inline-block;
            padding-right: 3px;
            vertical-align: middle;
            font-weight: 900;
        }
        """,
):
    st.button("Button with icon")

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

if st.button("https://pics.freeicons.io/uploads/icons/png/3536210891586786419-512.png"):
    st.write("TO DO")
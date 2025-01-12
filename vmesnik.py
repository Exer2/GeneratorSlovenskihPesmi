import streamlit as st
from streamlit.components.v1 import html
from generator import generator_pesmi
from stt import record_audio, recognize_speech


def generate_poem(word):
    pesem = generator_pesmi(word)
    return pesem

st.title("Pesmopisec")

# Initializacija stanja seje
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False

# Gumb za snemanje
def toggle_recording():
    if not st.session_state.is_recording:
        st.session_state.is_recording = True
        try:
            with st.spinner("Snemanje..."):
                transcript = record_audio()
                st.session_state.input_text = transcript
        except Exception as e:
            st.error(f"Napaka pri snemanju: {e}")
        finally:
            st.session_state.is_recording = False

# UI za vnos besede
col1, col2 = st.columns([3, 1])

with col1:
    word = st.text_input("bla", 
                         label_visibility="collapsed", 
                         placeholder="Vnesite ključno besedo...",
                         key="input_text",
                         value=st.session_state.input_text)

with col2:
    if st.button("🎙️ Snemaj", key="record_button", disabled=st.session_state.is_recording):
        toggle_recording()

# Gumb za generiranje pesmi
if st.button("Generiraj pesem"):
    if word:
        poem = generate_poem(word)
        st.text_area("Vaša pesem:", poem, height=500)
    else:
        st.error("Vnesite ključno besedo!")


if st.button("Začni snemanje"):
        audio_file = record_audio()  # Klicanje funkcije za snemanje zvoka
        st.write("Snemanje zaključeno! Zdaj prepoznavanje govora...")
        transcript = recognize_speech(audio_file)  # Klicanje funkcije za prepoznavanje govora
        st.write(f"Prepoznano besedilo: {transcript}")

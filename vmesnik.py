import streamlit as st
from generator import generator_pesmi

# Uporabniški vmesnik V1

# Funkcija za generiranje pesmi
def generate_poem(word):
    pesem = generator_pesmi(word)
    return pesem

# Dodamo prilagojeno HTML kodo za mikrofon
st.markdown("""
    <style>
    .input-with-microphone {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .microphone-icon {
        cursor: pointer;
        font-size: 24px;
        color: #6c757d;
    }
    </style>
    <script>
    function startSpeechRecognition() {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'sl-SI'; // Nastavi jezik na slovenščino
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById("keyword-input").value = transcript;
        };
        recognition.start();
    }
    </script>
""", unsafe_allow_html=True)

st.title("Pesmopisec")
st.markdown("""
    <div class="input-with-microphone">
        <input id="keyword-input" placeholder="Vpišite ključno besedo" style="width: calc(100% - 50px); padding: 5px;" />
        <span class="microphone-icon" onclick="startSpeechRecognition()">🎤</span>
    </div>
""", unsafe_allow_html=True)

# Uporabniška interakcija
if st.button("Generiraj pesem"):
    word = st.session_state.get("keyword-input", "")  # Preberi ključno besedo iz JavaScript
    if word:
        poem = generate_poem(word)
        st.text_area("Vaša pesem:", poem, height=500)
    else:
        st.error("Vnesite ključno besedo!")

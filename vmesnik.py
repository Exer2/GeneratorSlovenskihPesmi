import streamlit as st
from streamlit.components.v1 import html
from generator import generator_pesmi
from stt import glasovni_vnos

def generate_poem(word):
    pesem = generator_pesmi(word)
    return pesem

st.title("Pesmopisec")

# Initialize session state
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'recording_clicked' not in st.session_state:
    st.session_state.recording_clicked = False

def start_recording():
    st.session_state.recording_clicked = True

col1, col2 = st.columns([3, 1])

with col1:
    word = st.text_input("bla", 
                        label_visibility="collapsed", 
                        placeholder="Vnesite ključno besedo...",
                        key="input_text",
                        value=st.session_state.input_text)

with col2:
    # Custom HTML/CSS for the microphone button
    html("""
    <style>
    .icon-button {
        background-color: transparent;
        border: none;
        cursor: pointer;
        padding: 8px;
        border-radius: 10px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        margin-top: -8px;
        margin-left: -5px
    }
    .icon-button svg {
        width: 24px;
        height: 24px;
        fill: #6c757d;
    }
    .icon-button:hover svg {
        fill: #007bff;
    }
    </style>
    <button class="icon-button" id="micButton" onclick="window.microphone_clicked()">
        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 16 16" style="enable-background:new 0 0 16 16;" xml:space="preserve">
            <path d="M8,11c1.657,0,3-1.343,3-3V3c0-1.657-1.343-3-3-3S5,1.343,5,3v5C5,9.657,6.343,11,8,11z"></path>
            <path d="M13,8V6h-1l0,1.844c0,1.92-1.282,3.688-3.164,4.071C6.266,12.438,4,10.479,4,8V6H3v2c0,2.414,1.721,4.434,4,4.899V15H5v1h6
    v-1H9v-2.101C11.279,12.434,13,10.414,13,8z"></path>
        </svg>
    </button>
    <script>
    window.microphone_clicked = function() {
        window.parent.postMessage({type: 'microphone_clicked'}, '*');
    }
    </script>
    """, height=50)

    if st.button("Start Recording", key="hidden_rec_button"):
        try:
            with st.spinner("Snemanje..."):
                transcript = glasovni_vnos()
                st.session_state.input_text = transcript
                st.experimental_rerun()
        except Exception as e:
            st.error(f"Napaka pri snemanju: {e}")

# Add JavaScript to trigger the hidden button when microphone is clicked
st.markdown("""
<script>
window.addEventListener('message', function(e) {
    if (e.data.type === 'microphone_clicked') {
        document.querySelector('button[kind="secondary"]').click();
    }
}, false);
</script>
""", unsafe_allow_html=True)

if st.button("Generiraj pesem"):
    if word:
        poem = generate_poem(word)
        st.text_area("Vaša pesem:", poem, height=500)
    else:
        st.error("Vnesite ključno besedo!")
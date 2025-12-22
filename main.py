import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load local .env (for local dev)
load_dotenv()

# Get key (Cloud → st.secrets | Local → .env)
API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not found. Add it in Streamlit Secrets or .env")
    st.stop()

gen_ai.configure(api_key=API_KEY)

# Model
model = gen_ai.GenerativeModel("gemini-1.5-flash")

# Streamlit UI
st.set_page_config(
    page_title="Chat with Gemini",
    page_icon="🧠",
    layout="centered",
)

st.title("🤖 GemAI")

def translate_role_for_streamlit(role):
    return "assistant" if role == "model" else role

# Chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# History
for msg in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(msg.role)):
        st.markdown(msg.parts[0].text)

# User input
user_prompt = st.chat_input("Ask anything...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)

    reply = st.session_state.chat_session.send_message(user_prompt)

    with st.chat_message("assistant"):
        st.markdown(reply.text)


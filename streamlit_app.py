import streamlit as st
import tempfile
import os
import requests
import numpy as np

# Set page config
st.set_page_config(page_title="PDF Agent Assistant", layout="wide")

# Check Ollama is running
def is_ollama_available():
    try:
        r = requests.get("http://localhost:11434")
        return r.status_code == 200
    except:
        return False

if not is_ollama_available():
    st.error("❌ Ollama is not running. Please start it using `ollama serve`.")
    st.stop()

# Load modern theme
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# App imports
from app.logger import setup_logger
from app.tools.extractor import extract_text_from_pdf
from app.tools.semantic_chat import embed_chunks, answer_question_with_context
from app.memory import save_session, load_sessions, export_sessions_to_csv
from app.agent import plan_and_execute

logger = setup_logger()

# Title
st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=120)
st.markdown('<div class="big-title">PDF Agent Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Upload PDFs, generate summaries or quizzes, and chat with your document.</div>', unsafe_allow_html=True)

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chunk_embeddings" not in st.session_state:
    st.session_state.chunk_embeddings = None
if "chunks" not in st.session_state:
    st.session_state.chunks = None

# Helper
def split_text(text, chunk_size=500, overlap=50):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size - overlap)]

# Upload block
with st.container():
    st.header("📄 Upload a PDF")
    uploaded_file = st.file_uploader("Choose your PDF file", type=["pdf"])

# Main logic block
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        path = tmp_file.name

    with st.container():
        st.header("🧠 What would you like me to do?")
        selected_tasks = st.multiselect("Choose one or more tasks", ["Summarize Document", "Generate Quiz"])

    if st.button("🚀 Run Agent", use_container_width=True):
        with st.spinner("🤖 Processing your PDF..."):
            try:
                text = extract_text_from_pdf(path)
                chunks = split_text(text)
                embeddings = embed_chunks(chunks)

                st.session_state.chunks = chunks
                st.session_state.chunk_embeddings = embeddings

                output = ""
                if selected_tasks:
                    output = plan_and_execute(selected_tasks, text)
                    with st.container():
                        st.header("🧾 Agent Output")
                        st.markdown(output if output else "⚠️ No output was generated.")

                save_session(uploaded_file.name, ", ".join(selected_tasks), output)
                st.success("✅ Done! You can now chat with your document.")

            except Exception as e:
                logger.error("Agent failed", exc_info=True)
                st.error(f"❌ Error: {e}")

# Chat block at bottom
embeddings = st.session_state.get("chunk_embeddings")
if isinstance(embeddings, np.ndarray) and embeddings.size > 0:
    with st.container():
        st.header("🧠 Conversation")
        for sender, msg in st.session_state.chat_history[::-1]:
            css_class = "chat-user" if sender == "You" else "chat-agent"
            st.markdown(f"<div class='{css_class}'>{msg}</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 💬 Ask a question about this PDF")

        with st.form("chat_form", clear_on_submit=True):
            question = st.text_input("Type your question here", key="chat_input_form")
            submitted = st.form_submit_button("Send")

            if submitted and question:
                response = answer_question_with_context(question, st.session_state.chunks, embeddings)
                st.session_state.chat_history.append(("You", question))
                st.session_state.chat_history.append(("Agent", response))
                st.session_state["__trigger_rerun__"] = True

    # Trigger rerun after form to refresh chat
    if st.session_state.get("__trigger_rerun__"):
        del st.session_state["__trigger_rerun__"]
        st.rerun()

# Session logs
with st.expander("🗂️ Past Sessions"):
    sessions = load_sessions()
    if sessions:
        for s in sessions[::-1]:
            st.markdown(f"**{s['pdf']}** — {s['task']}")
            st.markdown(s['output'])
            st.markdown("---")
        if st.button("📤 Export Sessions"):
            export_sessions_to_csv()
            st.success("Exported to sessions.csv")
    else:
        st.info("No previous sessions found.")

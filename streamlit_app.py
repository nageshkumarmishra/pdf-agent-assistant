import streamlit as st
from app.tools.extractor import extract_text_from_pdf
from app.agent import plan_and_execute
from app.memory import save_session, load_sessions, export_sessions_to_csv
from app.logger import setup_logger

from app.tools.semantic_chat import (
    embed_chunks,
    answer_question_with_context
)

import tempfile
import os

# 🟡 Fix for PyTorch path bug on some Macs
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

# Setup
logger = setup_logger()
st.set_page_config(page_title="PDF Agent Assistant", layout="centered")
st.title("🤖 PDF Agent Assistant")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chunk_embeddings" not in st.session_state:
    st.session_state.chunk_embeddings = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

# Upload
uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf"])
selected_tasks = st.multiselect(
    "🧠 What would you like the assistant to do?",
    ["Summarize Document", "Generate Quiz"]
)

# Text splitter (manual, avoids langchain)
def split_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# Agent execution
if uploaded_file and selected_tasks:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_pdf_path = tmp_file.name

        with st.spinner("🔍 Processing..."):
            extracted_text = extract_text_from_pdf(tmp_pdf_path)
            chunks = split_text(extracted_text)
            st.session_state.chunks = chunks
            st.session_state.chunk_embeddings = embed_chunks(chunks)

            output = plan_and_execute(selected_tasks, extracted_text)
            st.success("✅ Task Completed!")
            st.markdown(output)

            save_session(uploaded_file.name, ", ".join(selected_tasks), output)
            os.unlink(tmp_pdf_path)

    except Exception as e:
        logger.exception("Agent workflow failed")
        st.error(f"❌ Error: {str(e)}")

# Chat interface
if st.session_state.chunk_embeddings is not None:
    st.markdown("### 💬 Chat with your PDF")
    user_input = st.text_input("Ask a question:")

    if user_input:
        response = answer_question_with_context(
            user_input,
            st.session_state.chunks,
            st.session_state.chunk_embeddings
        )
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Agent", response))

    for sender, msg in st.session_state.chat_history[::-1]:
        st.markdown(f"**{sender}:** {msg}")

# History
with st.expander("📂 View Past Sessions"):
    sessions = load_sessions()
    if sessions:
        for session in sessions[::-1]:
            st.markdown(f"**File:** {session['pdf']}")
            st.markdown(f"**Task:** {session['task']}")
            st.markdown(f"**Output:**\n\n{session['output']}")
            st.markdown("---")
        if st.button("📤 Export Sessions to CSV"):
            export_sessions_to_csv()
            st.success("Exported to sessions.csv")
    else:
        st.info("No past sessions found.")
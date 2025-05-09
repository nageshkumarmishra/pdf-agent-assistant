# streamlit_app.py
# Main entry point for the PDF summarizer Streamlit app

import streamlit as st
from app.extractor import extract_text_from_pdf
from app.summarizer import summarize_text
from app.logger import setup_logger
import tempfile
import os

# Set up logger
logger = setup_logger()

# Streamlit app configuration
st.set_page_config(page_title="PDF Summarizer", layout="centered")
st.title("📄 PDF Summarizer with Local AI (Ollama)")
st.markdown("Upload a PDF and get a concise summary powered by an open-source LLM running locally.")

# Upload file section
uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file:
    try:
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_pdf_path = tmp_file.name

        # Extract text from the uploaded PDF
        st.info("Extracting text from PDF...")
        text = extract_text_from_pdf(tmp_pdf_path)

        if not text.strip():
            st.warning("Could not extract any text from the PDF.")
        else:
            st.success("Text extracted successfully!")

            # Show a preview of extracted text
            with st.expander("Preview Extracted Text"):
                st.text_area("Extracted Text", value=text, height=200)

            # Button to summarize the text
            if st.button("Summarize PDF"):
                with st.spinner("Summarizing with Ollama LLM..."):
                    try:
                        summary = summarize_text(text)
                        st.success("Summary generated!")
                        st.text_area("Summary", value=summary, height=200)

                        # Option to download summary
                        st.download_button("Download Summary", summary, file_name="summary.txt")
                    except Exception as e:
                        logger.exception("Error during summarization")
                        st.error(f"Failed to summarize the text: {str(e)}")

        # Clean up temp file
        os.unlink(tmp_pdf_path)

    except Exception as e:
        logger.exception("Error handling uploaded PDF")
        st.error(f"An error occurred: {str(e)}")

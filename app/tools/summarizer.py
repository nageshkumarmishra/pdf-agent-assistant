# --- app/summarizer.py ---
# Interfaces with a local Ollama model to generate summaries

import ollama

def summarize_text(text):
    """
    Uses a local LLM (e.g., Mistral via Ollama) to summarize the given text.
    """
    prompt = f"Summarize the following document:\n\n{text[:3000]}"
    try:
        response = ollama.chat(
            model='mistral',  # Change model here if needed
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']
    except Exception as e:
        raise RuntimeError(f"LLM summarization failed: {str(e)}")

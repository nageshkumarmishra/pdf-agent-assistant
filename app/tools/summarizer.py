import ollama

def summarize_text(text):
    prompt = f"Summarize the following:\n\n{text[:3000]}"
    try:
        response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        return f"❌ Summarization failed: {str(e)}. Make sure Ollama is installed and running."
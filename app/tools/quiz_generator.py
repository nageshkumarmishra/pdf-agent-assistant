import ollama

def generate_quiz(text):
    """
    Generates a 5-question quiz from the given text using Ollama LLM.
    """
    prompt = f"Create 5 quiz questions from the following text:\n\n{text[:3000]}"
    response = ollama.chat(
        model='mistral',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content']

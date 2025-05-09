import ollama

def answer_query(text, question):
    """
    Answers a question based on the given document text using Ollama.
    """
    prompt = f"Answer the question based on this document:\n\n{text[:3000]}\n\nQuestion: {question}"
    response = ollama.chat(
        model='mistral',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content']
import ollama

def generate_quiz(text):
    prompt = f"Generate a quiz for the following:\n\n{text[:3000]}"
    try:
        response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        return f"❌ Quiz generation failed: {str(e)}. Ensure Ollama is running."
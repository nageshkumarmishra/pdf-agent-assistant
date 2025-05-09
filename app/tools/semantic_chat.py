from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import ollama

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks):
    return model.encode(chunks)

def is_question_relevant(question, chunk_embeddings, threshold=0.3):
    q_vec = model.encode([question])
    sims = cosine_similarity(q_vec, chunk_embeddings)
    return max(sims[0]) >= threshold

def get_best_context_chunks(question, chunks, chunk_embeddings, top_k=3):
    q_vec = model.encode([question])
    sims = cosine_similarity(q_vec, chunk_embeddings)[0]
    top_indices = sims.argsort()[-top_k:][::-1]
    return [chunks[i] for i in top_indices]

def answer_question_with_context(question, chunks, chunk_embeddings):
    if not is_question_relevant(question, chunk_embeddings):
        return "❌ Your question seems unrelated to the uploaded PDF."

    context = "\n\n".join(get_best_context_chunks(question, chunks, chunk_embeddings))
    prompt = f"Use this context to answer:\n\n{context}\n\nQuestion: {question}"
    try:
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        return f"❌ LLM failed to answer: {str(e)}. Make sure Ollama is installed and running."
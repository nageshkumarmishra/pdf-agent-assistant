# 📄 PDF Agent Assistant

An interactive AI-powered assistant that lets you:
- Upload any PDF document
- Get smart summaries or quizzes
- Chat with the document content using natural language

Built with **Streamlit**, **LangChain**, and **Ollama** for local LLM inference.

---

## 🚀 Features

✅ Upload PDFs easily  
✅ Select tasks: summarization, quiz generation  
✅ Chat with your PDF in a conversational UI  
✅ Stores past sessions and chat history  
✅ Runs **locally** with no external APIs

---

## 🧰 Tech Stack

- [Streamlit](https://streamlit.io) for the UI  
- [LangChain](https://www.langchain.com) for agent planning  
- [Ollama](https://ollama.com) for local LLM backend  
- Sentence Transformers (for embeddings)  
- Python 3.9+

---

## 📦 Installation

```bash
git clone https://github.com/your-username/pdf-agent-assistant.git
cd pdf-agent-assistant
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 🔧 Setup

1. **Start Ollama**:
   ```bash
   ollama serve
   ```

2. **Run the app**:
   ```bash
   streamlit run streamlit_app.py
   ```

---

## 💬 Usage

- Upload a PDF
- Select tasks (summarization, quiz)
- Click **"Run Agent"**
- Chat with the document at the bottom of the page

---

## 📁 Folder Structure

```
.
├── .streamlit/                # Streamlit configuration (optional)
├── .venv/                     # Python virtual environment (excluded by .gitignore)
├── app/
│   ├── agent.py               # Main agent workflow
│   ├── logger.py              # Logging setup
│   ├── memory.py              # Chat memory and persistence
│   └── tools/
│       ├── extractor.py       # PDF text extractor
│       ├── qa.py              # Question answering logic
│       ├── quiz_generator.py  # Quiz generation module
│       ├── semantic_chat.py   # Embedding + context-aware Q&A
│       └── summarizer.py      # Summarization logic
├── assets/
│   ├── style.css              # Custom Streamlit styling
├── memory.json                # Stored sessions (auto-generated)
├── requirements.txt           # Python dependencies
├── streamlit_app.py           # Main Streamlit UI
└── README.md                  # Project documentation
```

---

## 📜 License

MIT License — free to use and modify. Attribution appreciated!

---

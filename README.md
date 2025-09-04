# Café RAG Chatbot (Pro)

Modern Streamlit UI with sidebar preferences + MiniLM (embeddings) + FAISS retrieval + DistilBERT QA (grounded answers).

## Quickstart
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Notes
- Sidebar filters drive both the suggestions and the menu list.
- QA model gives concise answers; intent rules ensure hours/menu/price/suggest behave reliably.

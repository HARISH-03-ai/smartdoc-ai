import os
from pypdf import PdfReader
from docx import Document
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from config import Config

load_dotenv()
chroma_client = chromadb.PersistentClient(path="chroma_db")
model = SentenceTransformer(Config.EMBEDDING_MODEL)
api_key=os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

collection = chroma_client.get_or_create_collection(
    name="rag_collection"
    )

def read_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        return text
    
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
        
    elif ext == ".docx":
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    
    elif ext == ".csv":
        df = pd.read_csv(file_path)
        return df.to_string()
    
    elif ext == ".xlsx":
        df = pd.read_excel(file_path)
        return df.to_string()
    
    else:
        return "Unsupported file format"


def chunk_text(text):
    chunk_size = Config.CHUNK_SIZE
    overlap = Config.CHUNK_OVERLAP

    chunks = []

    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i+chunk_size]

        if chunk.strip():
            chunks.append(chunk)

    return chunks


def build_index(chunks):

    try:
        collection.delete(ids=collection.get()["ids"])
    except Exception as e:
        print(e)

    vectors = model.encode(chunks).tolist()

    ids = [str(i) for i in range(len(chunks))]

    collection.add(
        embeddings=vectors,
        documents=chunks,
        ids=ids
    )


def search_chunks(query):

    documents = collection.get()["documents"]

    stop_words = {
    "is", "there", "any", "with",
    "the", "if", "yes", "then",
    "tell", "me", "what", "who"
    }

    query_words = [
    word for word in query.lower().split()
    if word not in stop_words
    ]

    # Exact keyword matching
    for chunk in documents:

        match_count = 0
        chunk_words = chunk.lower().split()

        for word in query_words:

            if word in chunk_words:
                match_count += 1

        # if many words matched
        if match_count >= 3:
            return chunk

    # Semantic search fallback
    query_vector = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_vector,
        n_results=Config.TOP_K_RESULTS
    )

    context = ""

    for i in results["documents"][0]:
        context += i + "\n"

    return context


def ask_llm(context, query, chat_history):

    history_text = ""

    for chat in chat_history[-5:]:

        history_text += f"""
User: {chat['user']}
AI: {chat['ai']}
"""

    prompt = f"""
You are an intelligent AI assistant.

Rules:
- Use conversation history if relevant
- Use provided document context
- If answer is not found in context, say:
  "Not found in uploaded documents."

Previous Conversation:
{history_text}

Document Context:
{context}

Current User Question:
{query}
"""
    
    
    client = OpenAI(
    api_key= api_key,
    base_url= Config.GROQ_BASE_URL
    )
    
    response = client.chat.completions.create(model=Config.LLM_MODEL, messages=[{"role" : "user", "content" : prompt}], temperature=0.3, max_tokens=800)
    return response.choices[0].message.content
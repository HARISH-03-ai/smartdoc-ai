import os

class Config:

    UPLOAD_FOLDER = "uploads"

    MAX_CONTENT_LENGTH = 50 * 1024 * 1024

    CHUNK_SIZE = 1500

    CHUNK_OVERLAP = 300

    TOP_K_RESULTS = 3

    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

    LLM_MODEL = "llama-3.3-70b-versatile"

    GROQ_BASE_URL = "https://api.groq.com/openai/v1"
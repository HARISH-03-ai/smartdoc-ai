# SmartDoc AI

A Conversational Multi-Document RAG (Retrieval-Augmented Generation) Assistant built using Flask, ChromaDB, MySQL Authentication, and Groq LLM.

## Features

* User Signup & Login Authentication
* Secure Password Hashing using bcrypt
* Session Management using Flask Sessions
* User-Specific Document Storage
* Upload Multiple Documents
* Supports PDF, DOCX, TXT, CSV and XLSX
* Conversational AI Chat
* Retrieval-Augmented Generation (RAG)
* Semantic Search using Embeddings
* Exact Keyword Matching Fallback
* Chat History Support
* Modern Responsive UI

---

## Tech Stack

### Backend

* Python
* Flask
* MySQL
* bcrypt

### AI & RAG

* ChromaDB
* SentenceTransformers
* Groq LLM

### Frontend

* HTML
* CSS
* JavaScript

---

## Project Architecture

1. User Authentication
2. Document Upload
3. Text Extraction
4. Text Chunking
5. Embedding Generation
6. ChromaDB Indexing
7. Semantic Retrieval
8. Context Construction
9. LLM Response Generation

---

## Authentication Flow

1. User signs up with email and password
2. Password is hashed using bcrypt
3. User logs in
4. Flask session is created
5. User documents are loaded automatically
6. ChromaDB index is rebuilt for the logged-in user
7. User can query previously uploaded documents

---

## Document Processing Pipeline

```text
Upload File
    ↓
Extract Text
    ↓
Chunk Text
    ↓
Generate Embeddings
    ↓
Store in ChromaDB
    ↓
User Query
    ↓
Retrieve Relevant Chunks
    ↓
Send Context to Groq LLM
    ↓
Generate Response
```

---

## Multi-User Design

Each user has a dedicated upload directory:

```text
uploads/
├── 1/
├── 2/
├── 3/
```

Benefits:

* User-specific document storage
* Separate document management
* Session-based document loading
* Persistent user experience

---

## Challenges Faced

* PDF text extraction inconsistencies
* Semantic retrieval limitations
* Exact record retrieval from structured PDFs
* Hybrid retrieval implementation
* Session management
* User-specific document restoration after login

---

## Installation

Clone the repository:

```bash
git clone https://github.com/HARISH-03-ai/smartdoc-ai.git

cd smartdoc-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
SECRET_KEY=your_secret_key
```

Run the application:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Future Improvements

* OCR Support
* Better Table-Aware Retrieval
* Cloud Deployment
* Streaming AI Responses
* User Profile Management
* Document Deletion Dashboard
* Per-User ChromaDB Collections

---

## Screenshots

### Login Page

![Login Page](static/images/Login.png)

### Signup Page

![Signup Page](static/images/Signup.png)

### Homepage & AI Response

![Homepage](static/images/Homepage.png)

---

## Author

Harish Vishwakarma

Built using Flask, MySQL, ChromaDB, SentenceTransformers, and Groq LLM to explore Retrieval-Augmented Generation (RAG), Authentication Systems, and Multi-User AI Applications.

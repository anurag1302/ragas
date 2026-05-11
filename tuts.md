End-to-End RAG Tutorial in Python (Without LangChain)
Using:
TXT Files
FastAPI
ChromaDB
OpenRouter Embeddings
OpenRouter Chat Models
React Frontend
Goal

We will build a complete beginner-friendly RAG application.

The app will:

Upload .txt files
Split text into chunks
Generate embeddings using OpenRouter
Store vectors in ChromaDB
Search relevant chunks
Send context to an LLM
Return AI answers
Use a React frontend

We will NOT use LangChain.

This helps us understand how RAG actually works internally.

Final Architecture
React Frontend
↓
FastAPI Backend
↓
TXT File Upload
↓
Chunking
↓
OpenRouter Embeddings
↓
ChromaDB
↓
Similarity Search
↓
OpenRouter Chat Model
↓
Final Answer
What Is RAG?

RAG means:

Retrieval Augmented Generation

Instead of training the LLM with our data:

We search relevant information
Send it to the LLM
LLM answers using that context
Example

Suppose our TXT file contains:

Python was created by Guido van Rossum.

User asks:

Who created Python?

RAG flow:

1. Find relevant chunk
2. Send chunk to LLM
3. Generate answer
   Project Structure
   rag-app/
   │
   ├── backend/
   │ ├── app/
   │ │ ├── main.py
   │ │ ├── chunking.py
   │ │ ├── embeddings.py
   │ │ ├── chroma_service.py
   │ │ ├── llm_service.py
   │ │ ├── document_processor.py
   │ │ └── models.py
   │ │
   │ ├── uploads/
   │ ├── chroma_db/
   │ ├── requirements.txt
   │ └── .env
   │
   └── frontend/
   PART 1 — Backend Setup
   Step 1 — Create Project
   mkdir rag-app
   cd rag-app

mkdir backend
cd backend
Step 2 — Create Virtual Environment
Mac/Linux
python3 -m venv venv
source venv/bin/activate
Windows
python -m venv venv
venv\Scripts\activate
Step 3 — Install Dependencies

Create:

requirements.txt

Add:

fastapi
uvicorn
python-multipart
chromadb
openai
python-dotenv

Install:

pip install -r requirements.txt
Why These Packages?
Package Purpose
fastapi API framework
uvicorn Runs FastAPI server
python-multipart File uploads
chromadb Vector database
openai OpenRouter/OpenAI SDK
python-dotenv Environment variables
Step 4 — Create Folders
mkdir app
mkdir uploads
mkdir chroma_db
PART 2 — Understanding Embeddings
What Is An Embedding?

Embedding means:

Text → Numbers

Example:

"I love Python"

becomes:

[0.123, 0.983, 0.222, ...]

These numbers represent meaning.

Why Embeddings?

Because vector databases cannot understand text directly.

They understand vectors.

PART 3 — Chunking

Create:

app/chunking.py

Code:

import re

def find_last_sentence_break(text):

    matches = list(re.finditer(r"[.!?]", text))


    if not matches:
        return -1


    return matches[-1].start()

def split_text(text, chunk_size=1000, overlap=200):

    chunks = []


    start = 0


    while start < len(text):


        end = start + chunk_size


        if end >= len(text):
            chunks.append(text[start:].strip())
            break


        window = text[start:end]


        sentence_break = find_last_sentence_break(window)


        if sentence_break != -1:
            actual_end = start + sentence_break + 1
        else:
            actual_end = end


        chunk = text[start:actual_end].strip()


        if chunk:
            chunks.append(chunk)


        start = actual_end - overlap


        if start < 0:
            start = 0


    return chunks

What This Code Does

This code:

Splits large text
Creates smaller chunks
Keeps overlap
Tries to break near sentences
Why Overlap Is Important

Without overlap:

context may break

Overlap helps preserve meaning between chunks.

PART 4 — OpenRouter Embeddings

Create:

app/embeddings.py

Code:

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
api_key=os.getenv("OPENROUTER_API_KEY"),
base_url="https://openrouter.ai/api/v1"
)

EMBEDDING_MODEL = "text-embedding-3-small"

def create_embedding(text):

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )


    return response.data[0].embedding

Important Note

Even though we are using OpenRouter SDK endpoint:

text-embedding-3-small

is still an OpenAI embeddings model.

OpenRouter acts as the gateway.

What Happens Here?
Step 1
client = OpenAI(...)

Creates OpenRouter client.

Step 2
client.embeddings.create(...)

Sends text to embeddings model.

Step 3

Model returns vector.

Example:

[0.123, 0.777, 0.111, ...]
PART 5 — ChromaDB

Create:

app/chroma_service.py

Code:

import chromadb
import uuid

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
name="documents"
)

def add_documents(chunks, embeddings):

    ids = []


    for _ in chunks:
        ids.append(str(uuid.uuid4()))


    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )

def search_documents(query_embedding, top_k=3):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )


    return results

What Is ChromaDB?

ChromaDB is a vector database.

Instead of storing normal rows:

id | name

It stores:

id | vector
Why Vector Search?

Normal search uses keywords.

Vector search uses meaning.

Example:

"How to lose fat"

can match:

"weight reduction methods"

because meanings are similar.

PART 6 — TXT File Reader

Create:

app/document_processor.py

Code:

def extract_text_from_txt(file_path):

    with open(file_path, "r", encoding="utf-8") as file:


        text = file.read()


    return text

What This Does
Opens text file
Reads content
Returns text

Very simple.

PART 7 — OpenRouter Chat Model

Create:

app/llm_service.py

Code:

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
api_key=os.getenv("OPENROUTER_API_KEY"),
base_url="https://openrouter.ai/api/v1"
)

CHAT_MODEL = "deepseek/deepseek-chat-v3-0324:free"

def ask_llm(question, context):

    prompt = f"""

You are a helpful AI assistant.

Answer the question ONLY using the provided context.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response.choices[0].message.content

VERY IMPORTANT RAG CONCEPT

The REAL power of RAG is:

Question + Retrieved Context

Without context:

LLM may hallucinate.

With context:

LLM answers from documents.

PART 8 — Request Models

Create:

app/models.py

Code:

from pydantic import BaseModel

class ChatRequest(BaseModel):
question: str
PART 9 — Main FastAPI Application

Create:

app/main.py

Code:

from fastapi import FastAPI, UploadFile, File
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

@app.get("/")
def home():
return {
"message": "RAG API Running"
}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"


    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)


    text = extract_text_from_txt(file_path)


    chunks = split_text(text)


    embeddings = []


    for chunk in chunks:


        embedding = create_embedding(chunk)


        embeddings.append(embedding)


    add_documents(chunks, embeddings)


    return {
        "message": "Document uploaded successfully",
        "chunks_created": len(chunks)
    }

@app.post("/chat")
def chat(request: ChatRequest):

    question_embedding = create_embedding(request.question)


    results = search_documents(question_embedding)


    documents = results["documents"][0]


    context = "\n\n".join(documents)


    answer = ask_llm(request.question, context)


    return {
        "question": request.question,
        "answer": answer,
        "context": documents
    }

Understanding Full RAG Flow
Upload Flow
TXT File
↓
Extract Text
↓
Chunk Text
↓
Generate Embeddings
↓
Store In ChromaDB
Chat Flow
User Question
↓
Question Embedding
↓
Vector Search
↓
Retrieve Relevant Chunks
↓
Send Context To LLM
↓
Generate Final Answer
PART 10 — Environment Variables

Create:

.env

Add:

OPENROUTER_API_KEY=your_api_key_here
PART 11 — Run Backend
uvicorn app.main:app --reload
Swagger UI

Open:

http://localhost:8000/docs

FastAPI automatically gives API testing UI.

Test Upload

Use:

POST /upload

Upload a .txt file.

Test Chat

Example:

{
"question": "What is this document about?"
}
PART 12 — React Frontend
Create Frontend

Go to root folder:

cd ..

Create React app:

npm create vite@latest frontend -- --template react
Install Dependencies
cd frontend
npm install
npm install axios
PART 13 — React App

Replace:

src/App.jsx

Code:

import { useState } from "react"
import axios from "axios"

function App() {

const [file, setFile] = useState(null)
const [question, setQuestion] = useState("")
const [answer, setAnswer] = useState("")
const [loading, setLoading] = useState(false)

const uploadFile = async () => {

    if (!file) {
      alert("Select a file")
      return
    }

I created a complete markdown-style beginner-friendly RAG tutorial using:

TXT files
FastAPI
ChromaDB
OpenRouter embeddings
OpenRouter chat models
React frontend
No LangChain

It includes:

detailed explanations
project structure
step-by-step code
chunking explanation
embeddings explanation
vector search flow
full backend/frontend integration
easy-to-understand architecture diagrams

All written in beginner-friendly style for learning fundamentals deeply.

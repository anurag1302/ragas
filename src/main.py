import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from src.chunks import split_text
from src.embeds import create_embedding
from src.chromaDBService import add_documents, search_documents
from src.llmService import ask_llm
from src.documentLoader import extract_text
import os
from src.models import ChatRequest
import logging
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RAG Fast API")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/bootstrap")
async def bootstrap():
    return "Success"


@app.post("/upload")
async def upload(file: UploadFile = File()):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    _, extension = os.path.splitext(file.filename)
    # text = content.decode("utf-8")
    text = extract_text(file_path, extension)
    # logger.info(f"File name:{file.filename}, File size:{len(content)}")
    # logger.info(f"File content:{text[:400]}")
    chunks = split_text(text, chunk_size=1000, overlap=200)

    embeddings = []
    metadatas = []
    for index, chunk in chunks:
        embedding = create_embedding(chunk)
        embeddings.append(embedding)
        metadatas.append({"file_name": file.filename, "chunk_id": index, "text": chunk})

    add_documents(chunks, embeddings, metadatas)

    return {
        "message": "Document Uploaded Successfully",
        "number of chunks created": len(chunks),
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    question_embedding = create_embedding(request.question)
    results = search_documents(question_embedding)
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = "\n\n".join(documents)

    sources = []
    for document, metadata in zip(document, metadatas):
        sources.append(
            {
                "text": document,
                "file_name": metadata["file_name"],
                "chunk_id": metadata["chunk_id"],
            }
        )

    answer = ask_llm(request.question, context)

    return {"question": request.question, "answer": answer, "sources": sources}

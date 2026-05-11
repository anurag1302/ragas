import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from src.chunks import split_text
from src.embeds import create_embedding
from src.chromaDBService import add_documents
import logging

app = FastAPI(title="RAG Fast API")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/chat")
async def notChat():
    return "Success"


@app.post("/upload")
async def upload(file: UploadFile = File()):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    text = content.decode("utf-8")
    # logger.info(f"File name:{file.filename}, File size:{len(content)}")
    # logger.info(f"File content:{text[:400]}")
    chunks = split_text(text, chunk_size=1000, overlap=200)

    embeddings = []
    for chunk in chunks:
        embedding = create_embedding(chunk)
        embeddings.append(embedding)

    add_documents(chunks, embeddings)

    return {
        "message": "Document Uploaded Successfully",
        "number of chunks created": len(chunks),
    }

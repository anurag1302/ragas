import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from src.chunks import split_text
import logging

app = FastAPI(title="RAG Fast API")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/chat")
async def notChat():
    return "Success"


@app.post("/upload")
async def upload(file: UploadFile = File()):
    content = await file.read()
    text = content.decode("utf-8")
    logger.info(f"File name:{file.filename}, File size:{len(content)}")
    logger.info(f"File content:{text[:400]}")
    split_text(text, chunk_size=500, chunk_overlap=100)
    return "Success"

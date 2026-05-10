import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

app = FastAPI(title="RAG Fast API")


@app.get("/chat", status_code=200)
async def chat():
    return "Success"

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from app.config import settings
from app.ingest import DocumentProcessor
from app.vectorstore import VectorStore
from app.retriever import Retriever


app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

processor = DocumentProcessor()
vectorstore = VectorStore()
retriever = Retriever()


class ChatRequest(BaseModel):
    query: str
    chat_history: list[dict] | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]
    scores: list[float]


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in [".pdf", ".txt", ".md"]:
        raise HTTPException(400, f"Unsupported file type: {suffix}")

    file_path = settings.UPLOAD_DIR / file.filename
    content = await file.read()
    file_path.write_bytes(content)

    try:
        chunks = processor.process_file(file_path)
        vectorstore.add_documents(chunks)
        return {
            "filename": file.filename,
            "chunks": len(chunks),
            "status": "success",
        }
    except Exception as e:
        raise HTTPException(500, f"Processing failed: {str(e)}")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = retriever.retrieve(request.query, request.chat_history)
    return ChatResponse(
        answer=result.answer,
        sources=result.sources,
        scores=result.scores,
    )


@app.get("/stats")
def get_stats():
    return vectorstore.get_stats()


@app.delete("/collection")
def delete_collection():
    vectorstore.delete_collection()
    return {"status": "deleted"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

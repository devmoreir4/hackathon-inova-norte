from typing import List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.application.services.rag_service import RAGService

rag_router = APIRouter(prefix="/rag", tags=["AI RAG Chat"])

class ChatMessage(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    sources: List[str] = []

rag_service = RAGService()

@rag_router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with AI",
    description="Chat with AI - automatically processes documents from data/documents/ folder"
)
def chat(chat_message: ChatMessage):
    try:
        result = rag_service.chat(chat_message.message)
        return ChatResponse(
            response=result["response"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in chat: {str(e)}"
        )

@rag_router.get(
    "/status",
    summary="Get RAG status",
    description="Check RAG system status and loaded files"
)
def get_status():
    try:
        return rag_service.get_status()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting status: {str(e)}"
        )

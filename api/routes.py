# api/routes.py

from fastapi import APIRouter, HTTPException
from orchestrator.orchestrator import AgentOrchestrator
from api.schemas import ChatRequest, ChatResponse

from config import logger


router = APIRouter()

# Initialize orchestrator
orchestrator = AgentOrchestrator()

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from orchestrator.orchestrator import AgentOrchestrator

router = APIRouter()
orchestrator = AgentOrchestrator()

@router.post("/chat")
async def chat_endpoint(payload: dict):
    user_message = payload.get("message", "")
    if not user_message:
        return JSONResponse({"error": "No message provided"}, status_code=400)
    
    # Call orchestrator to process all agents
    response = orchestrator.handle_message(user_message)
    return JSONResponse(response)


@router.get("/health")
def health_check():

    return {
        "status": "running",
        "service": "agentic-food-chatbot"
    }
# main.py

from fastapi import FastAPI
from api.routes import router
from config import logger

import uvicorn


app = FastAPI(
    title="Agentic AI Food Ordering API",
    description="Multi-Agent LangGraph Food Ordering Chatbot",
    version="1.0"
)


app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Agentic AI Food Ordering System Running"
    }


if __name__ == "__main__":

    logger.info("Starting Food Agentic AI Server")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
# api/schemas.py

from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    session_id: str


class OrderRequest(BaseModel):
    user_id: str
    session_id: str
    order_message: str


class OrderResponse(BaseModel):
    order_id: Optional[str]
    status: str
    details: Optional[dict]


class TrackOrderRequest(BaseModel):
    order_id: str
    user_id: str


class TrackOrderResponse(BaseModel):
    order_id: str
    eta: str
    status: str
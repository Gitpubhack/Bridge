"""
Support Ticket schemas
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from models.ticket import TicketStatus, TicketPriority

class MessageCreate(BaseModel):
    user_id: int
    ticket_id: int
    message: str
    attachments: Optional[List[str]] = None

class TicketCreate(BaseModel):
    user_id: int
    subject: str
    category: str
    priority: TicketPriority = TicketPriority.MEDIUM
    message: str
    related_transaction_id: Optional[int] = None
    related_order_id: Optional[int] = None

class TicketResponse(BaseModel):
    id: int
    user_id: int
    subject: str
    category: str
    priority: TicketPriority
    status: TicketStatus
    messages: Optional[List[Dict[str, Any]]]
    assigned_to: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class TicketListResponse(BaseModel):
    tickets: List[TicketResponse]
    total: int
    page: int
    per_page: int

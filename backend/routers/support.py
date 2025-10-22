"""
Support router for Bridge Exchange
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from database import get_db
from models.ticket import Ticket, TicketStatus, TicketPriority
from schemas.ticket import TicketCreate, TicketResponse, MessageCreate, TicketListResponse
from routers.auth import get_current_user

router = APIRouter()

@router.post("/ticket")
async def create_ticket(
    request: TicketCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create support ticket"""
    try:
        # Create ticket
        ticket = Ticket(
            user_id=current_user["id"],
            subject=request.subject,
            category=request.category,
            priority=request.priority,
            status=TicketStatus.OPEN,
            messages=[{
                "user_id": current_user["id"],
                "message": request.message,
                "timestamp": "2023-01-01T00:00:00Z",
                "attachments": []
            }]
        )
        
        db.add(ticket)
        await db.commit()
        await db.refresh(ticket)
        
        return TicketResponse(
            id=ticket.id,
            user_id=ticket.user_id,
            subject=ticket.subject,
            category=ticket.category,
            priority=ticket.priority,
            status=ticket.status,
            messages=ticket.messages,
            assigned_to=ticket.assigned_to,
            created_at=ticket.created_at,
            updated_at=ticket.updated_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create ticket"
        )

@router.post("/message")
async def add_message(
    request: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Add message to ticket"""
    try:
        # Get ticket
        result = await db.execute(
            select(Ticket).where(Ticket.id == request.ticket_id)
        )
        ticket = result.scalar_one_or_none()
        
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found"
            )
        
        # Add message
        if not ticket.messages:
            ticket.messages = []
        
        ticket.messages.append({
            "user_id": current_user["id"],
            "message": request.message,
            "timestamp": "2023-01-01T00:00:00Z",
            "attachments": request.attachments or []
        })
        
        await db.commit()
        
        return {"success": True, "message": "Message added"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add message"
        )

@router.get("/tickets")
async def get_user_tickets(
    page: int = 1,
    per_page: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get user tickets"""
    try:
        offset = (page - 1) * per_page
        
        result = await db.execute(
            select(Ticket)
            .where(Ticket.user_id == current_user["id"])
            .order_by(Ticket.created_at.desc())
            .offset(offset)
            .limit(per_page)
        )
        tickets = result.scalars().all()
        
        # Get total count
        count_result = await db.execute(
            select(Ticket).where(Ticket.user_id == current_user["id"])
        )
        total = len(count_result.scalars().all())
        
        return TicketListResponse(
            tickets=[
                TicketResponse(
                    id=t.id,
                    user_id=t.user_id,
                    subject=t.subject,
                    category=t.category,
                    priority=t.priority,
                    status=t.status,
                    messages=t.messages,
                    assigned_to=t.assigned_to,
                    created_at=t.created_at,
                    updated_at=t.updated_at
                )
                for t in tickets
            ],
            total=total,
            page=page,
            per_page=per_page
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get tickets"
        )

"""
DAO schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.dao_proposal import ProposalStatus

class DAOProposalCreate(BaseModel):
    created_by: int
    title: str
    description: str
    voting_duration_days: int = 7

class DAOProposalResponse(BaseModel):
    id: int
    title: str
    description: str
    created_by: int
    status: ProposalStatus
    votes_for: int
    votes_against: int
    total_votes: int
    quorum_met: bool
    created_at: datetime
    voting_ends_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class VoteRequest(BaseModel):
    user_id: int
    proposal_id: int
    vote: bool  # True for "for", False for "against"

class ProposalListResponse(BaseModel):
    proposals: list[DAOProposalResponse]
    total: int
    page: int
    per_page: int

"""
DAO Proposal model for Bridge Exchange
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Enum
from sqlalchemy.sql import func
from database import Base
import enum

class ProposalStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PASSED = "passed"
    REJECTED = "rejected"
    EXECUTED = "executed"

class DAOProposal(Base):
    __tablename__ = "dao_proposals"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_by = Column(Integer, nullable=False, index=True)
    status = Column(Enum(ProposalStatus), default=ProposalStatus.DRAFT)
    votes_for = Column(Integer, default=0)
    votes_against = Column(Integer, default=0)
    total_votes = Column(Integer, default=0)
    quorum_met = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    voting_ends_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<DAOProposal(id={self.id}, title={self.title}, status={self.status}, votes_for={self.votes_for})>"

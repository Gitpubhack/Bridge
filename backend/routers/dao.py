"""
DAO router for Bridge Exchange
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta

from database import get_db
from models.dao_proposal import DAOProposal, ProposalStatus
from schemas.dao import DAOProposalCreate, DAOProposalResponse, VoteRequest, ProposalListResponse
from routers.auth import get_current_user

router = APIRouter()

@router.post("/proposal")
async def create_proposal(
    request: DAOProposalCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create DAO proposal"""
    try:
        # Create proposal
        proposal = DAOProposal(
            created_by=current_user["id"],
            title=request.title,
            description=request.description,
            status=ProposalStatus.ACTIVE,
            voting_ends_at=datetime.utcnow() + timedelta(days=request.voting_duration_days)
        )
        
        db.add(proposal)
        await db.commit()
        await db.refresh(proposal)
        
        return DAOProposalResponse(
            id=proposal.id,
            title=proposal.title,
            description=proposal.description,
            created_by=proposal.created_by,
            status=proposal.status,
            votes_for=proposal.votes_for,
            votes_against=proposal.votes_against,
            total_votes=proposal.total_votes,
            quorum_met=proposal.quorum_met,
            created_at=proposal.created_at,
            voting_ends_at=proposal.voting_ends_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create proposal"
        )

@router.post("/vote")
async def vote_on_proposal(
    request: VoteRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Vote on DAO proposal"""
    try:
        # Get proposal
        result = await db.execute(
            select(DAOProposal).where(DAOProposal.id == request.proposal_id)
        )
        proposal = result.scalar_one_or_none()
        
        if not proposal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proposal not found"
            )
        
        if proposal.status != ProposalStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Proposal not active"
            )
        
        if proposal.voting_ends_at and datetime.utcnow() > proposal.voting_ends_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Voting period ended"
            )
        
        # Update votes (simplified - in production, check for duplicate votes)
        if request.vote:
            proposal.votes_for += 1
        else:
            proposal.votes_against += 1
        
        proposal.total_votes += 1
        
        # Check quorum (simplified)
        if proposal.total_votes >= 10:  # Minimum quorum
            proposal.quorum_met = True
            
            # Determine result
            if proposal.votes_for > proposal.votes_against:
                proposal.status = ProposalStatus.PASSED
            else:
                proposal.status = ProposalStatus.REJECTED
        
        await db.commit()
        
        return {"success": True, "vote": request.vote}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to vote"
        )

@router.get("/proposals")
async def get_proposals(
    page: int = 1,
    per_page: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """Get DAO proposals"""
    try:
        offset = (page - 1) * per_page
        
        result = await db.execute(
            select(DAOProposal)
            .order_by(DAOProposal.created_at.desc())
            .offset(offset)
            .limit(per_page)
        )
        proposals = result.scalars().all()
        
        # Get total count
        count_result = await db.execute(select(DAOProposal))
        total = len(count_result.scalars().all())
        
        return ProposalListResponse(
            proposals=[
                DAOProposalResponse(
                    id=p.id,
                    title=p.title,
                    description=p.description,
                    created_by=p.created_by,
                    status=p.status,
                    votes_for=p.votes_for,
                    votes_against=p.votes_against,
                    total_votes=p.total_votes,
                    quorum_met=p.quorum_met,
                    created_at=p.created_at,
                    voting_ends_at=p.voting_ends_at
                )
                for p in proposals
            ],
            total=total,
            page=page,
            per_page=per_page
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get proposals"
        )

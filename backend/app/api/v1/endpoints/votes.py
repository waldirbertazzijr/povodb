from typing import Any, List, Optional
from uuid import UUID
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from app.db.session import get_db
from app.models.vote import Vote
from app.schemas.vote.vote import (
    Vote as VoteSchema,
    VoteCreate,
    VoteUpdate,
    VotePage,
    VoteWithRelations,
)

router = APIRouter()


@router.get("", response_model=VotePage, summary="Get votes")
async def read_votes(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Skip items"),
    limit: int = Query(100, ge=1, le=100, description="Limit items"),
    politician_id: Optional[UUID] = Query(None, description="Filter by politician ID"),
    bill_id: Optional[UUID] = Query(None, description="Filter by bill ID"),
    vote_position: Optional[str] = Query(None, description="Filter by vote position"),
    vote_result: Optional[str] = Query(None, description="Filter by vote result"),
    from_date: Optional[date] = Query(None, description="Filter votes from this date"),
    to_date: Optional[date] = Query(None, description="Filter votes to this date"),
) -> Any:
    """
    Retrieve votes with pagination and filtering options.
    """
    query = select(Vote)

    # Apply filters
    if politician_id:
        query = query.filter(Vote.politician_id == politician_id)
    if bill_id:
        query = query.filter(Vote.bill_id == bill_id)
    if vote_position:
        query = query.filter(Vote.vote_position == vote_position)
    if vote_result:
        query = query.filter(Vote.vote_result == vote_result)
    if from_date:
        query = query.filter(Vote.vote_date >= from_date)
    if to_date:
        query = query.filter(Vote.vote_date <= to_date)

    # Get count
    count_query = select(func.count()).select_from(Vote)
    if politician_id:
        count_query = count_query.filter(Vote.politician_id == politician_id)
    if bill_id:
        count_query = count_query.filter(Vote.bill_id == bill_id)
    if vote_position:
        count_query = count_query.filter(Vote.vote_position == vote_position)
    if vote_result:
        count_query = count_query.filter(Vote.vote_result == vote_result)
    if from_date:
        count_query = count_query.filter(Vote.vote_date >= from_date)
    if to_date:
        count_query = count_query.filter(Vote.vote_date <= to_date)

    result = await db.execute(count_query)
    total_count = result.scalar_one()

    # Apply pagination
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    items = result.scalars().all()

    # Calculate pagination values
    total_pages = (total_count + limit - 1) // limit if total_count > 0 else 0
    current_page = skip // limit + 1 if skip % limit == 0 else skip // limit + 1

    return {
        "items": items,
        "total": total_count,
        "page": current_page,
        "size": limit,
        "pages": total_pages,
    }


@router.get("/{id}", response_model=VoteWithRelations, summary="Get vote by ID")
async def read_vote(
    *,
    db: AsyncSession = Depends(get_db),
    id: UUID = Path(..., description="The UUID of the vote"),
) -> Any:
    """
    Get a specific vote by ID with related politician and bill information.
    """
    query = (
        select(Vote)
        .options(
            joinedload(Vote.politician),
            joinedload(Vote.bill)
        )
        .filter(Vote.id == id)
    )
    result = await db.execute(query)
    db_obj = result.scalars().first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="Vote not found")

    return db_obj


@router.post("", response_model=VoteSchema, status_code=201, summary="Create vote")
async def create_vote(
    *,
    db: AsyncSession = Depends(get_db),
    vote_in: VoteCreate,
) -> Any:
    """
    Create a new vote record.
    """
    db_obj = Vote(**vote_in.dict())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)

    return db_obj


@router.put("/{id}", response_model=VoteSchema, summary="Update vote")
async def update_vote(
    *,
    db: AsyncSession = Depends(get_db),
    id: UUID = Path(..., description="The UUID of the vote"),
    vote_in: VoteUpdate,
) -> Any:
    """
    Update a vote record.
    """
    query = select(Vote).filter(Vote.id == id)
    result = await db.execute(query)
    db_obj = result.scalars().first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="Vote not found")

    update_data = vote_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)

    return db_obj


@router.delete("/{id}", response_model=VoteSchema, summary="Delete vote")
async def delete_vote(
    *,
    db: AsyncSession = Depends(get_db),
    id: UUID = Path(..., description="The UUID of the vote"),
) -> Any:
    """
    Delete a vote record.
    """
    query = select(Vote).filter(Vote.id == id)
    result = await db.execute(query)
    db_obj = result.scalars().first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="Vote not found")

    await db.delete(db_obj)
    await db.commit()

    return db_obj


@router.get("/statistics/by-politician", summary="Get vote statistics by politician")
async def vote_statistics_by_politician(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(10, ge=1, le=100, description="Limit results"),
) -> Any:
    """
    Get voting statistics grouped by politician.
    """
    from sqlalchemy import func, case, distinct
    from app.models.politician import Politician

    query = (
        select(
            Politician.id,
            Politician.name,
            Politician.party,
            func.count(Vote.id).label("total_votes"),
            func.count(case([(Vote.vote_position == "yea", 1)])).label("yea_votes"),
            func.count(case([(Vote.vote_position == "nay", 1)])).label("nay_votes"),
            func.count(distinct(Vote.bill_id)).label("bills_voted")
        )
        .join(Vote, Vote.politician_id == Politician.id)
        .group_by(Politician.id, Politician.name, Politician.party)
        .order_by(func.count(Vote.id).desc())
        .limit(limit)
    )

    result = await db.execute(query)
    stats = result.all()

    return [
        {
            "politician_id": str(row[0]),
            "politician_name": row[1],
            "party": row[2],
            "total_votes": row[3],
            "yea_votes": row[4],
            "nay_votes": row[5],
            "bills_voted": row[6],
            "yea_percentage": round(row[4] / row[3] * 100, 2) if row[3] > 0 else 0,
        }
        for row in stats
    ]

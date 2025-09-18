from typing import Any, List, Optional
from uuid import UUID
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from app.db.session import get_db
from app.models.political_contribution import PoliticalContribution
from app.schemas.contribution.contribution import (
    Contribution as ContributionSchema,
    ContributionCreate,
    ContributionUpdate,
    ContributionPage,
    ContributionWithPolitician,
)

router = APIRouter()


@router.get("", response_model=ContributionPage, summary="Get contributions")
async def read_contributions(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Skip items"),
    limit: int = Query(100, ge=1, le=100, description="Limit items"),
    politician_id: Optional[UUID] = Query(None, description="Filter by politician ID"),
    contributor_name: Optional[str] = Query(None, description="Filter by contributor name"),
    contributor_type: Optional[str] = Query(None, description="Filter by contributor type"),
    min_amount: Optional[float] = Query(None, ge=0, description="Minimum contribution amount"),
    max_amount: Optional[float] = Query(None, ge=0, description="Maximum contribution amount"),
    from_date: Optional[date] = Query(None, description="Filter contributions from this date"),
    to_date: Optional[date] = Query(None, description="Filter contributions to this date"),
) -> Any:
    """
    Retrieve political contributions with pagination and filtering options.
    """
    query = select(PoliticalContribution)

    # Apply filters
    if politician_id:
        query = query.filter(PoliticalContribution.politician_id == politician_id)
    if contributor_name:
        query = query.filter(PoliticalContribution.contributor_name.ilike(f"%{contributor_name}%"))
    if contributor_type:
        query = query.filter(PoliticalContribution.contributor_type == contributor_type)
    if min_amount is not None:
        query = query.filter(PoliticalContribution.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(PoliticalContribution.amount <= max_amount)
    if from_date:
        query = query.filter(PoliticalContribution.contribution_date >= from_date)
    if to_date:
        query = query.filter(PoliticalContribution.contribution_date <= to_date)

    # Get count
    count_query = select(func.count()).select_from(PoliticalContribution)
    if politician_id:
        count_query = count_query.filter(PoliticalContribution.politician_id == politician_id)
    if contributor_name:
        count_query = count_query.filter(PoliticalContribution.contributor_name.ilike(f"%{contributor_name}%"))
    if contributor_type:
        count_query = count_query.filter(PoliticalContribution.contributor_type == contributor_type)
    if min_amount is not None:
        count_query = count_query.filter(PoliticalContribution.amount >= min_amount)
    if max_amount is not None:
        count_query = count_query.filter(PoliticalContribution.amount <= max_amount)
    if from_date:
        count_query = count_query.filter(PoliticalContribution.contribution_date >= from_date)
    if to_date:
        count_query = count_query.filter(PoliticalContribution.contribution_date <= to_date)

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


@router.get("/{id}", response_model=ContributionWithPolitician, summary="Get contribution by ID")
async def read_contribution(
    *,
    db: AsyncSession = Depends(get_db),
    id: UUID = Path(..., description="The UUID of the contribution"),
) -> Any:
    """
    Get a specific contribution by ID with related politician information.
    """
    query = (
        select(PoliticalContribution)
        .options(joinedload(PoliticalContribution.politician))
        .filter(PoliticalContribution.id == id)
    )
    result = await db.execute(query)
    db_obj = result.scalars().first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="Contribution not found")

    return db_obj


@router.post("", response_model=ContributionSchema, status_code=201, summary="Create contribution")
async def create_contribution(
    *,
    db: AsyncSession = Depends(get_db),
    contribution_in: ContributionCreate,
) -> Any:
    """
    Create a new contribution record.
    """
    db_obj = PoliticalContribution(**contribution_in.dict())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)

    return db_obj


@router.put("/{id}", response_model=ContributionSchema, summary="Update contribution")
async def update_contribution(
    *,
    db: AsyncSession = Depends(get_db),
    id: UUID = Path(..., description="The UUID of the contribution"),
    contribution_in: ContributionUpdate,
) -> Any:
    """
    Update a contribution record.
    """
    query = select(PoliticalContribution).filter(PoliticalContribution.id == id)
    result = await db.execute(query)
    db_obj = result.scalars().first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="Contribution not found")

    update_data = contribution_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)

    return db_obj


@router.delete("/{id}", response_model=ContributionSchema, summary="Delete contribution")
async def delete_contribution(
    *,
    db: AsyncSession = Depends(get_db),
    id: UUID = Path(..., description="The UUID of the contribution"),
) -> Any:
    """
    Delete a contribution record.
    """
    query = select(PoliticalContribution).filter(PoliticalContribution.id == id)
    result = await db.execute(query)
    db_obj = result.scalars().first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="Contribution not found")

    await db.delete(db_obj)
    await db.commit()

    return db_obj


@router.get("/statistics/top-contributors", summary="Get top contributors")
async def top_contributors(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(10, ge=1, le=100, description="Limit results"),
) -> Any:
    """
    Get statistics about top contributors across all politicians.
    """
    query = (
        select(
            PoliticalContribution.contributor_name,
            PoliticalContribution.contributor_type,
            func.sum(PoliticalContribution.amount).label("total_amount"),
            func.count().label("contribution_count"),
            func.count(func.distinct(PoliticalContribution.politician_id)).label("politicians_supported")
        )
        .group_by(
            PoliticalContribution.contributor_name,
            PoliticalContribution.contributor_type
        )
        .order_by(func.sum(PoliticalContribution.amount).desc())
        .limit(limit)
    )

    result = await db.execute(query)
    stats = result.all()

    return [
        {
            "contributor_name": row[0],
            "contributor_type": row[1],
            "total_amount": float(row[2]),
            "contribution_count": row[3],
            "politicians_supported": row[4],
            "average_contribution": float(row[2]) / row[3] if row[3] > 0 else 0,
        }
        for row in stats
    ]

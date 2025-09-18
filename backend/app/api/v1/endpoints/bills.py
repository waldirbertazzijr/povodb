from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.bill import Bill
from app.schemas.bill.bill import (
    Bill as BillSchema,
    BillCreate,
    BillUpdate,
    BillPage,
    BillWithSponsor,
)

router = APIRouter()


@router.get("", response_model=BillPage, summary="Get bills")
async def read_bills(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Skip items"),
    limit: int = Query(100, ge=1, le=100, description="Limit items"),
    status: Optional[str] = Query(None, description="Filter by status"),
    sponsor_id: Optional[UUID] = Query(None, description="Filter by sponsor ID"),
) -> Any:
    """
    Retrieve bills with pagination and filtering options.
    """
    # For now, return a simple response
    # In a real implementation, we would use proper CRUD methods
    from sqlalchemy import select, func
    from sqlalchemy.orm import joinedload

    query = select(Bill)

    # Apply filters
    if status:
        query = query.filter(Bill.status == status)
    if sponsor_id:
        query = query.filter(Bill.sponsor_id == sponsor_id)

    # Get count
    count_query = select(func.count()).select_from(Bill)
    if status:
        count_query = count_query.filter(Bill.status == status)
    if sponsor_id:
        count_query = count_query.filter(Bill.sponsor_id == sponsor_id)

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


@router.get("/{id}", response_model=BillWithSponsor, summary="Get bill by ID")
async def read_bill(
    *,
    db: AsyncSession = Depends(get_db),
    id: UUID = Path(..., description="The UUID of the bill"),
) -> Any:
    """
    Get a specific bill by ID.
    """
    from sqlalchemy import select
    from sqlalchemy.orm import joinedload

    query = select(Bill).options(joinedload(Bill.sponsor)).filter(Bill.id == id)
    result = await db.execute(query)
    db_obj = result.scalars().first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="Bill not found")

    return db_obj


@router.post("", response_model=BillSchema, status_code=201, summary="Create bill")
async def create_bill(
    *,
    db: AsyncSession = Depends(get_db),
    bill_in: BillCreate,
) -> Any:
    """
    Create a new bill.
    """
    # Simple implementation for now
    from sqlalchemy.dialects.postgresql import insert

    db_obj = Bill(**bill_in.dict())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)

    return db_obj


@router.put("/{id}", response_model=BillSchema, summary="Update bill")
async def update_bill(
    *,
    db: AsyncSession = Depends(get_db),
    id: UUID = Path(..., description="The UUID of the bill"),
    bill_in: BillUpdate,
) -> Any:
    """
    Update a bill.
    """
    from sqlalchemy import select

    query = select(Bill).filter(Bill.id == id)
    result = await db.execute(query)
    db_obj = result.scalars().first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="Bill not found")

    update_data = bill_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)

    return db_obj


@router.delete("/{id}", response_model=BillSchema, summary="Delete bill")
async def delete_bill(
    *,
    db: AsyncSession = Depends(get_db),
    id: UUID = Path(..., description="The UUID of the bill"),
) -> Any:
    """
    Delete a bill.
    """
    from sqlalchemy import select

    query = select(Bill).filter(Bill.id == id)
    result = await db.execute(query)
    db_obj = result.scalars().first()

    if not db_obj:
        raise HTTPException(status_code=404, detail="Bill not found")

    await db.delete(db_obj)
    await db.commit()

    return db_obj

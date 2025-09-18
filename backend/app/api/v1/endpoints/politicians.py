from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.db.session import get_db
from app.crud.crud_politician import politician
from app.schemas.politician.politician import (
    Politician,
    PoliticianCreate,
    PoliticianUpdate,
    PoliticianPage,
    PoliticianDetail,
)

router = APIRouter()


@router.get("", response_model=PoliticianPage, summary="Get politicians")
async def read_politicians(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Skip items"),
    limit: int = Query(100, ge=1, le=100, description="Limit items"),
    name: Optional[str] = Query(None, description="Filter by name (partial match)"),
    party: Optional[str] = Query(None, description="Filter by party"),
    country: Optional[str] = Query(None, description="Filter by country"),
    state_province: Optional[str] = Query(None, description="Filter by state/province"),
) -> Any:
    """
    Retrieve politicians with pagination and filtering options.
    """
    try:
        items = await politician.get_by_filters(
            db,
            skip=skip,
            limit=limit,
            name=name,
            party=party,
            country=country,
            state_province=state_province
        )
        count = await politician.count(db)

        # Calculate pagination values
        total_pages = (count + limit - 1) // limit if count > 0 else 0
        current_page = skip // limit + 1 if skip % limit == 0 else skip // limit + 1

        return {
            "items": items,
            "total": count,
            "page": current_page,
            "size": limit,
            "pages": total_pages,
        }
    except SQLAlchemyError as e:
        logging.error(f"Database error when fetching politicians: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching politicians data from database"
        )
    except Exception as e:
        logging.error(f"Unexpected error in read_politicians: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.post("", response_model=Politician, status_code=201, summary="Create politician")
async def create_politician(
    *,
    db: AsyncSession = Depends(get_db),
    politician_in: PoliticianCreate,
) -> Any:
    """
    Create a new politician.
    """
    try:
        return await politician.create(db, obj_in=politician_in)
    except SQLAlchemyError as e:
        logging.error(f"Database error when creating politician: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating politician in database"
        )
    except Exception as e:
        logging.error(f"Unexpected error in create_politician: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.get("/{id}", response_model=Politician, summary="Get politician by ID")
async def read_politician(
    *,
    db: AsyncSession = Depends(get_db),
    id: UUID = Path(..., description="The UUID of the politician"),
) -> Any:
    """
    Get a specific politician by ID.
    """
    try:
        result = await politician.get(db, id=id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Politician not found"
            )
        return result
    except SQLAlchemyError as e:
        logging.error(f"Database error when fetching politician ID {id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching politician data from database"
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Unexpected error in read_politician for ID {id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.get("/{id}/details", response_model=PoliticianDetail, summary="Get politician with related data")
async def read_politician_with_relations(
    *,
    db: AsyncSession = Depends(get_db),
    id: UUID = Path(..., description="The UUID of the politician"),
) -> Any:
    """
    Get a specific politician by ID with related data (votes, bills, contributions).
    """
    try:
        result = await politician.get_with_relations(db, id=id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Politician not found"
            )
        return result
    except SQLAlchemyError as e:
        logging.error(f"Database error when fetching politician relations for ID {id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching politician details from database"
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Unexpected error in read_politician_with_relations for ID {id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching politician details"
        )


@router.get("/{id}/contributions", summary="Get politician's contribution statistics")
async def read_politician_contributions(
    *,
    db: AsyncSession = Depends(get_db),
    id: UUID = Path(..., description="The UUID of the politician"),
) -> Any:
    """
    Get a specific politician with their contribution statistics.
    """
    result = await politician.get_with_contribution_stats(db, id=id)
    if not result:
        raise HTTPException(status_code=404, detail="Politician not found")
    return result


@router.put("/{id}", response_model=Politician, summary="Update politician")
async def update_politician(
    *,
    db: AsyncSession = Depends(get_db),
    id: UUID = Path(..., description="The UUID of the politician"),
    politician_in: PoliticianUpdate,
) -> Any:
    """
    Update a politician.
    """
    db_obj = await politician.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Politician not found")
    return await politician.update(db, db_obj=db_obj, obj_in=politician_in)


@router.delete("/{id}", response_model=Politician, summary="Delete politician")
async def delete_politician(
    *,
    db: AsyncSession = Depends(get_db),
    id: UUID = Path(..., description="The UUID of the politician"),
) -> Any:
    """
    Delete a politician.
    """
    db_obj = await politician.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Politician not found")
    return await politician.remove(db, id=id)

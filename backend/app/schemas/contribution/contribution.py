from typing import Optional, List
from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel, Field

from app.schemas.politician.politician import Politician


# Shared properties
class ContributionBase(BaseModel):
    """Base schema for political contribution data."""
    contributor_name: str
    contributor_type: Optional[str] = None
    amount: float = Field(..., gt=0)
    contribution_date: date


# Properties to receive on item creation
class ContributionCreate(ContributionBase):
    """Schema for creating a new political contribution."""
    politician_id: UUID


# Properties to receive on item update
class ContributionUpdate(BaseModel):
    """Schema for updating a political contribution."""
    contributor_name: Optional[str] = None
    contributor_type: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    contribution_date: Optional[date] = None


# Properties shared by models stored in DB
class ContributionInDBBase(ContributionBase):
    """Schema for contribution data from the database."""
    id: UUID
    politician_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Properties to return to client
class Contribution(ContributionInDBBase):
    """Schema for returning contribution data to clients."""
    pass


# Properties to return to client with related info
class ContributionWithPolitician(Contribution):
    """Schema for returning contribution data with politician information."""
    politician: Optional[Politician] = None


# Properties properties stored in DB
class ContributionInDB(ContributionInDBBase):
    """Schema for contribution data stored in the database with additional fields."""
    deleted_at: Optional[datetime] = None


# For pagination
class ContributionPage(BaseModel):
    """Schema for paginated contribution results."""
    items: List[Contribution]
    total: int
    page: int
    size: int
    pages: int

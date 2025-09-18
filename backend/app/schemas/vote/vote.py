from typing import Optional, List
from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel

from app.schemas.politician.politician import Politician
from app.schemas.bill.bill import Bill


# Shared properties
class VoteBase(BaseModel):
    """Base schema for vote data."""
    bill_title: str
    vote_date: date
    vote_position: str
    vote_result: str


# Properties to receive on item creation
class VoteCreate(VoteBase):
    """Schema for creating a new vote."""
    politician_id: UUID
    bill_id: UUID


# Properties to receive on item update
class VoteUpdate(BaseModel):
    """Schema for updating a vote."""
    bill_title: Optional[str] = None
    vote_date: Optional[date] = None
    vote_position: Optional[str] = None
    vote_result: Optional[str] = None


# Properties shared by models stored in DB
class VoteInDBBase(VoteBase):
    """Schema for vote data from the database."""
    id: UUID
    politician_id: UUID
    bill_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Properties to return to client
class Vote(VoteInDBBase):
    """Schema for returning vote data to clients."""
    pass


# Properties to return to client with related info
class VoteWithRelations(Vote):
    """Schema for returning vote data with politician and bill information."""
    politician: Optional[Politician] = None
    bill: Optional[Bill] = None


# Properties properties stored in DB
class VoteInDB(VoteInDBBase):
    """Schema for vote data stored in the database with additional fields."""
    deleted_at: Optional[datetime] = None


# For pagination
class VotePage(BaseModel):
    """Schema for paginated vote results."""
    items: List[Vote]
    total: int
    page: int
    size: int
    pages: int

from typing import Optional, List
from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl

from app.schemas.politician.politician import Politician


# Shared properties
class BillBase(BaseModel):
    """Base schema for bill data."""
    bill_number: str
    title: str
    description: Optional[str] = None
    introduced_date: Optional[date] = None
    status: Optional[str] = None
    full_text_url: Optional[HttpUrl] = None


# Properties to receive on item creation
class BillCreate(BillBase):
    """Schema for creating a new bill."""
    sponsor_id: Optional[UUID] = None


# Properties to receive on item update
class BillUpdate(BaseModel):
    """Schema for updating a bill."""
    bill_number: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    introduced_date: Optional[date] = None
    status: Optional[str] = None
    full_text_url: Optional[HttpUrl] = None
    sponsor_id: Optional[UUID] = None


# Properties shared by models stored in DB
class BillInDBBase(BillBase):
    """Schema for bill data from the database."""
    id: UUID
    sponsor_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Properties to return to client
class Bill(BillInDBBase):
    """Schema for returning bill data to clients."""
    pass


# Properties to return to client with sponsor info
class BillWithSponsor(Bill):
    """Schema for returning bill data with sponsor information."""
    sponsor: Optional[Politician] = None


# Properties properties stored in DB
class BillInDB(BillInDBBase):
    """Schema for bill data stored in the database with additional fields."""
    deleted_at: Optional[datetime] = None


# For pagination
class BillPage(BaseModel):
    """Schema for paginated bill results."""
    items: List[Bill]
    total: int
    page: int
    size: int
    pages: int

from typing import Optional, List, Union
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl

# Shared properties
class PoliticianBase(BaseModel):
    """Base schema for politician data."""
    name: str
    party: Optional[str] = None
    position: Optional[str] = None
    country: str
    state_province: Optional[str] = None
    bio: Optional[str] = None
    website: Optional[str] = None
    photo_url: Optional[HttpUrl] = None


# Properties to receive on item creation
class PoliticianCreate(PoliticianBase):
    """Schema for creating a new politician."""
    pass


# Properties to receive on item update
class PoliticianUpdate(BaseModel):
    """Schema for updating a politician."""
    name: Optional[str] = None
    party: Optional[str] = None
    position: Optional[str] = None
    country: Optional[str] = None
    state_province: Optional[str] = None
    bio: Optional[str] = None
    website: Optional[str] = None
    photo_url: Optional[HttpUrl] = None


# Properties shared by models stored in DB
class PoliticianInDBBase(PoliticianBase):
    """Schema for politician data from the database."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Properties to return to client
class Politician(PoliticianInDBBase):
    """Schema for returning politician data to clients."""
    pass


# Properties properties stored in DB
class PoliticianInDB(PoliticianInDBBase):
    """Schema for politician data stored in the database with additional fields."""
    deleted_at: Optional[datetime] = None


# For related models
class ContributionSchema(BaseModel):
    """Schema for contribution data in politician details."""
    id: UUID
    contributor_name: str
    contributor_type: Optional[str] = None
    amount: float
    contribution_date: datetime

    class Config:
        from_attributes = True

class VoteSchema(BaseModel):
    """Schema for vote data in politician details."""
    id: UUID
    bill_id: UUID
    bill_title: str
    vote_date: datetime
    vote_position: str
    vote_result: str

    class Config:
        from_attributes = True

class BillSchema(BaseModel):
    """Schema for bill data in politician details."""
    id: UUID
    bill_number: str
    title: str
    description: Optional[str] = None
    introduced_date: Optional[datetime] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True

# Schema for politician with detailed information
class PoliticianDetail(PoliticianInDBBase):
    """Schema for politician with related data."""
    votes: List[VoteSchema] = Field(default_factory=list)
    sponsored_bills: List[BillSchema] = Field(default_factory=list)
    contributions: List[ContributionSchema] = Field(default_factory=list)

    class Config:
        from_attributes = True

# For pagination
class PoliticianPage(BaseModel):
    """Schema for paginated politician results."""
    items: List[Politician]
    total: int
    page: int
    size: int
    pages: int

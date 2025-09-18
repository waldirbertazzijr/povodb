from typing import List, Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Politician(Base):
    """
    Model representing a politician.

    Contains basic information about politicians, their party affiliation,
    position, and biographical information.
    """

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    party: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    position: Mapped[Optional[str]] = mapped_column(String(255))
    country: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    state_province: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    bio: Mapped[Optional[str]] = mapped_column(Text)
    website: Mapped[Optional[str]] = mapped_column(String(255))
    photo_url: Mapped[Optional[str]] = mapped_column(String(255))

    # Relationships
    votes: Mapped[List["Vote"]] = relationship(
        "Vote", back_populates="politician", cascade="all, delete-orphan"
    )
    sponsored_bills: Mapped[List["Bill"]] = relationship(
        "Bill", back_populates="sponsor", foreign_keys="[Bill.sponsor_id]"
    )
    contributions: Mapped[List["PoliticalContribution"]] = relationship(
        "PoliticalContribution", back_populates="politician", cascade="all, delete-orphan"
    )

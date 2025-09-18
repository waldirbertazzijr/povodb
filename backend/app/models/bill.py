from typing import List, Optional
from datetime import date
from uuid import UUID
from sqlalchemy import String, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PgUUID

from app.db.base_class import Base


class Bill(Base):
    """
    Model representing a legislative bill.

    Contains information about bills, their status, sponsor, and related data.
    """

    bill_number: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    introduced_date: Mapped[Optional[date]] = mapped_column(Date, index=True)
    status: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    full_text_url: Mapped[Optional[str]] = mapped_column(String(255))

    # Foreign Keys
    sponsor_id: Mapped[Optional[UUID]] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("politician.id", ondelete="SET NULL"),
        index=True
    )

    # Relationships
    sponsor: Mapped[Optional["Politician"]] = relationship(
        "Politician", back_populates="sponsored_bills", foreign_keys=[sponsor_id]
    )
    votes: Mapped[List["Vote"]] = relationship(
        "Vote", back_populates="bill", cascade="all, delete-orphan"
    )

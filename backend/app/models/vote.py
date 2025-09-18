from typing import Optional
from datetime import date
from uuid import UUID
from sqlalchemy import String, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PgUUID

from app.db.base_class import Base


class Vote(Base):
    """
    Model representing a vote cast by a politician on a bill.

    Contains information about how a politician voted on a specific bill,
    including the date of the vote and the result.
    """

    # Foreign Keys
    politician_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("politician.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    bill_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("bill.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Vote data
    bill_title: Mapped[str] = mapped_column(Text, nullable=False)
    vote_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    vote_position: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="'yea', 'nay', 'present', 'not voting'"
    )
    vote_result: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="'passed', 'failed'"
    )

    # Relationships
    politician: Mapped["Politician"] = relationship(
        "Politician", back_populates="votes"
    )

    bill: Mapped["Bill"] = relationship(
        "Bill", back_populates="votes"
    )

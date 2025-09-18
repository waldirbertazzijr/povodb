from typing import Optional
from datetime import date
from uuid import UUID
from sqlalchemy import String, Numeric, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PgUUID

from app.db.base_class import Base


class PoliticalContribution(Base):
    """
    Model representing a political contribution to a politician.

    Contains information about financial contributions, including the contributor,
    amount, and date of the contribution.
    """
    __tablename__ = "political_contribution"

    # Foreign Keys
    politician_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("politician.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Contribution data
    contributor_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    contributor_type: Mapped[Optional[str]] = mapped_column(
        String(100),
        comment="'individual', 'PAC', 'party', etc."
    )
    amount: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        index=True
    )
    contribution_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    # Relationships
    politician: Mapped["Politician"] = relationship(
        "Politician", back_populates="contributions"
    )

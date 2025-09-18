from typing import List, Optional, Dict, Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.politician import Politician
from app.schemas.politician.politician import PoliticianCreate, PoliticianUpdate


class CRUDPolitician(CRUDBase[Politician, PoliticianCreate, PoliticianUpdate]):
    """CRUD operations for politicians."""

    async def get_with_relations(self, db: AsyncSession, id: UUID) -> Optional[Politician]:
        """
        Get a politician by ID with related data (votes, bills, contributions).

        Args:
            db: Database session
            id: UUID of the politician

        Returns:
            Politician with related data, or None if not found
        """
        query = (
            select(Politician)
            .options(
                selectinload(Politician.votes),
                selectinload(Politician.sponsored_bills),
                selectinload(Politician.contributions)
            )
            .where(Politician.id == id)
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_filters(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
        party: Optional[str] = None,
        country: Optional[str] = None,
        state_province: Optional[str] = None,
    ) -> List[Politician]:
        """
        Get politicians filtered by various criteria.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            name: Filter by name (case-insensitive, partial match)
            party: Filter by party (exact match)
            country: Filter by country (exact match)
            state_province: Filter by state/province (exact match)

        Returns:
            List of filtered politicians
        """
        query = select(Politician)

        # Apply filters
        if name:
            query = query.filter(Politician.name.ilike(f"%{name}%"))
        if party:
            query = query.filter(Politician.party == party)
        if country:
            query = query.filter(Politician.country == country)
        if state_province:
            query = query.filter(Politician.state_province == state_province)

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return result.scalars().all()

    async def get_with_contribution_stats(
        self, db: AsyncSession, id: UUID
    ) -> Optional[Dict[str, Any]]:
        """
        Get a politician with contribution statistics.

        Args:
            db: Database session
            id: UUID of the politician

        Returns:
            Dictionary with politician data and contribution stats, or None if not found
        """
        from sqlalchemy import func
        from app.models.political_contribution import PoliticalContribution

        # Get the politician
        politician = await self.get(db, id)
        if not politician:
            return None

        # Get contribution stats
        query = (
            select(
                func.sum(PoliticalContribution.amount).label("total_amount"),
                func.count().label("total_contributions"),
                func.avg(PoliticalContribution.amount).label("average_contribution")
            )
            .where(PoliticalContribution.politician_id == id)
        )
        result = await db.execute(query)
        stats = result.first()

        # Combine politician data with stats
        politician_data = politician.to_dict()
        politician_data["contribution_stats"] = {
            "total_amount": float(stats[0]) if stats[0] else 0,
            "total_contributions": stats[1] or 0,
            "average_contribution": float(stats[2]) if stats[2] else 0
        }

        return politician_data


politician = CRUDPolitician(Politician)

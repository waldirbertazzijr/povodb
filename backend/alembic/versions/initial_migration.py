"""initial migration

Revision ID: 1ae43b6ab40d
Revises:
Create Date: 2023-09-18 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1ae43b6ab40d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create politicians table
    op.create_table(
        'politician',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('party', sa.String(length=100), nullable=True),
        sa.Column('position', sa.String(length=255), nullable=True),
        sa.Column('country', sa.String(length=100), nullable=False),
        sa.Column('state_province', sa.String(length=100), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('photo_url', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_politician_country'), 'politician', ['country'], unique=False)
    op.create_index(op.f('ix_politician_name'), 'politician', ['name'], unique=False)
    op.create_index(op.f('ix_politician_party'), 'politician', ['party'], unique=False)
    op.create_index(op.f('ix_politician_state_province'), 'politician', ['state_province'], unique=False)

    # Create bills table
    op.create_table(
        'bill',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('bill_number', sa.String(length=100), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('introduced_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(length=100), nullable=True),
        sa.Column('full_text_url', sa.String(length=255), nullable=True),
        sa.Column('sponsor_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['sponsor_id'], ['politician.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bill_bill_number'), 'bill', ['bill_number'], unique=False)
    op.create_index(op.f('ix_bill_introduced_date'), 'bill', ['introduced_date'], unique=False)
    op.create_index(op.f('ix_bill_sponsor_id'), 'bill', ['sponsor_id'], unique=False)
    op.create_index(op.f('ix_bill_status'), 'bill', ['status'], unique=False)

    # Create votes table
    op.create_table(
        'vote',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('politician_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('bill_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('bill_title', sa.Text(), nullable=False),
        sa.Column('vote_date', sa.Date(), nullable=False),
        sa.Column('vote_position', sa.String(length=50), nullable=False),
        sa.Column('vote_result', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['bill_id'], ['bill.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['politician_id'], ['politician.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vote_bill_id'), 'vote', ['bill_id'], unique=False)
    op.create_index(op.f('ix_vote_politician_id'), 'vote', ['politician_id'], unique=False)
    op.create_index(op.f('ix_vote_vote_date'), 'vote', ['vote_date'], unique=False)

    # Create political_contribution table
    op.create_table(
        'political_contribution',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('politician_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('contributor_name', sa.String(length=255), nullable=False),
        sa.Column('contributor_type', sa.String(length=100), nullable=True),
        sa.Column('amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('contribution_date', sa.Date(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['politician_id'], ['politician.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_political_contribution_amount'), 'political_contribution', ['amount'], unique=False)
    op.create_index(op.f('ix_political_contribution_contribution_date'), 'political_contribution', ['contribution_date'], unique=False)
    op.create_index(op.f('ix_political_contribution_contributor_name'), 'political_contribution', ['contributor_name'], unique=False)
    op.create_index(op.f('ix_political_contribution_politician_id'), 'political_contribution', ['politician_id'], unique=False)


def downgrade() -> None:
    op.drop_table('political_contribution')
    op.drop_table('vote')
    op.drop_table('bill')
    op.drop_table('politician')

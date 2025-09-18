"""Initial tables for the political transparency database

Revision ID: 0001_initial_tables
Revises:
Create Date: 2023-11-14 14:35:12.982051

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision = '0001_initial_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create politician table
    op.create_table(
        'politician',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(255), nullable=False, index=True),
        sa.Column('party', sa.String(100), nullable=True, index=True),
        sa.Column('position', sa.String(255), nullable=True),
        sa.Column('country', sa.String(100), nullable=False, index=True),
        sa.Column('state_province', sa.String(100), nullable=True, index=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('website', sa.String(255), nullable=True),
        sa.Column('photo_url', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )

    # Create bill table
    op.create_table(
        'bill',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('bill_number', sa.String(100), nullable=False, index=True),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('introduced_date', sa.Date(), nullable=True, index=True),
        sa.Column('status', sa.String(100), nullable=True, index=True),
        sa.Column('full_text_url', sa.String(255), nullable=True),
        sa.Column('sponsor_id', postgresql.UUID(as_uuid=True),
                 sa.ForeignKey('politician.id', ondelete='SET NULL'),
                 nullable=True, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )

    # Create vote table
    op.create_table(
        'vote',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('politician_id', postgresql.UUID(as_uuid=True),
                 sa.ForeignKey('politician.id', ondelete='CASCADE'),
                 nullable=False, index=True),
        sa.Column('bill_id', postgresql.UUID(as_uuid=True),
                 sa.ForeignKey('bill.id', ondelete='CASCADE'),
                 nullable=False, index=True),
        sa.Column('bill_title', sa.Text(), nullable=False),
        sa.Column('vote_date', sa.Date(), nullable=False, index=True),
        sa.Column('vote_position', sa.String(50), nullable=False),
        sa.Column('vote_result', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )

    # Create political_contribution table
    op.create_table(
        'political_contribution',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('politician_id', postgresql.UUID(as_uuid=True),
                 sa.ForeignKey('politician.id', ondelete='CASCADE'),
                 nullable=False, index=True),
        sa.Column('contributor_name', sa.String(255), nullable=False, index=True),
        sa.Column('contributor_type', sa.String(100), nullable=True),
        sa.Column('amount', sa.Numeric(15, 2), nullable=False, index=True),
        sa.Column('contribution_date', sa.Date(), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )

    # Create indexes
    op.create_index('ix_politician_name_party', 'politician', ['name', 'party'])
    op.create_index('ix_politician_country_state', 'politician', ['country', 'state_province'])
    op.create_index('ix_bill_status_introduced', 'bill', ['status', 'introduced_date'])
    op.create_index('ix_vote_position_result', 'vote', ['vote_position', 'vote_result'])
    op.create_index('ix_contribution_amount_date', 'political_contribution', ['amount', 'contribution_date'])


def downgrade() -> None:
    op.drop_table('political_contribution')
    op.drop_table('vote')
    op.drop_table('bill')
    op.drop_table('politician')

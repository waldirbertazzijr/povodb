-- Direct database initialization script for PovoDB
-- This runs automatically when the PostgreSQL container starts

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create tables for political data

-- Table: politicians
CREATE TABLE IF NOT EXISTS politician (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    party VARCHAR(100),
    position VARCHAR(255),
    country VARCHAR(100) NOT NULL,
    state_province VARCHAR(100),
    bio TEXT,
    website VARCHAR(255),
    photo_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Table: bills
CREATE TABLE IF NOT EXISTS bill (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bill_number VARCHAR(100) NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    introduced_date DATE,
    status VARCHAR(100),
    sponsor_id UUID REFERENCES politician(id) ON DELETE SET NULL,
    full_text_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Table: votes
CREATE TABLE IF NOT EXISTS vote (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    politician_id UUID NOT NULL REFERENCES politician(id) ON DELETE CASCADE,
    bill_id UUID NOT NULL REFERENCES bill(id) ON DELETE CASCADE,
    bill_title TEXT NOT NULL,
    vote_date DATE NOT NULL,
    vote_position VARCHAR(50) NOT NULL, -- 'sim', 'não', 'presente', 'não votou'
    vote_result VARCHAR(50) NOT NULL, -- 'aprovado', 'reprovado'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Table: political_contributions
CREATE TABLE IF NOT EXISTS political_contribution (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    politician_id UUID NOT NULL REFERENCES politician(id) ON DELETE CASCADE,
    contributor_name VARCHAR(255) NOT NULL,
    contributor_type VARCHAR(100), -- 'Partido', 'Associação', 'Grupo Industrial', etc.
    amount DECIMAL(15, 2) NOT NULL,
    contribution_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_politician_name ON politician(name);
CREATE INDEX IF NOT EXISTS idx_politician_party ON politician(party);
CREATE INDEX IF NOT EXISTS idx_politician_country ON politician(country);
CREATE INDEX IF NOT EXISTS idx_politician_state_province ON politician(state_province);

CREATE INDEX IF NOT EXISTS idx_bill_bill_number ON bill(bill_number);
CREATE INDEX IF NOT EXISTS idx_bill_introduced_date ON bill(introduced_date);
CREATE INDEX IF NOT EXISTS idx_bill_status ON bill(status);
CREATE INDEX IF NOT EXISTS idx_bill_sponsor_id ON bill(sponsor_id);

CREATE INDEX IF NOT EXISTS idx_vote_politician_id ON vote(politician_id);
CREATE INDEX IF NOT EXISTS idx_vote_bill_id ON vote(bill_id);
CREATE INDEX IF NOT EXISTS idx_vote_vote_date ON vote(vote_date);

CREATE INDEX IF NOT EXISTS idx_contribution_politician_id ON political_contribution(politician_id);
CREATE INDEX IF NOT EXISTS idx_contribution_contributor_name ON political_contribution(contributor_name);
CREATE INDEX IF NOT EXISTS idx_contribution_amount ON political_contribution(amount);
CREATE INDEX IF NOT EXISTS idx_contribution_date ON political_contribution(contribution_date);

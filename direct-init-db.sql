-- Direct database initialization script for PovoDB
-- Run this script directly in the database container to set up the schema

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

-- Insert sample data
INSERT INTO politician (name, party, position, country, state_province, bio)
VALUES
    ('Luiz Inácio Lula da Silva', 'PT', 'Presidente', 'Brasil', 'São Paulo', 'Ex-metalúrgico e líder sindical, foi presidente do Brasil por dois mandatos (2003-2010) e eleito novamente em 2022.'),
    ('Arthur Lira', 'PP', 'Presidente da Câmara', 'Brasil', 'Alagoas', 'Deputado Federal desde 2011, eleito presidente da Câmara dos Deputados em 2021 e reeleito em 2023.'),
    ('Simone Tebet', 'MDB', 'Ministra', 'Brasil', 'Mato Grosso do Sul', 'Ex-senadora e atual Ministra do Planejamento, foi a terceira colocada na eleição presidencial de 2022.')
ON CONFLICT (id) DO NOTHING;

-- Get IDs for the politicians
DO $$
DECLARE
    lula_id UUID;
    lira_id UUID;
    tebet_id UUID;
BEGIN
    SELECT id INTO lula_id FROM politician WHERE name = 'Luiz Inácio Lula da Silva' LIMIT 1;
    SELECT id INTO lira_id FROM politician WHERE name = 'Arthur Lira' LIMIT 1;
    SELECT id INTO tebet_id FROM politician WHERE name = 'Simone Tebet' LIMIT 1;

    -- Insert bills
    INSERT INTO bill (bill_number, title, description, introduced_date, status, sponsor_id)
    VALUES
        ('PL-123/2023', 'Lei de Incentivo às Energias Renováveis', 'Projeto de lei que promove o desenvolvimento e infraestrutura de energia renovável no Brasil', '2023-01-15', 'Em Comissão', lula_id),
        ('PEC-456/2023', 'Reforma Orçamentária', 'Proposta de Emenda Constitucional para reforma abrangente do orçamento público', '2023-02-20', 'Aprovada na Câmara', lira_id),
        ('PL-789/2023', 'Lei de Desenvolvimento de Infraestrutura', 'Financiamento para projetos de infraestrutura críticos em todo o país', '2023-03-10', 'Apresentado', tebet_id)
    ON CONFLICT (id) DO NOTHING;

    -- Get bill IDs
    WITH bill_data AS (
        SELECT id, bill_number FROM bill
        WHERE bill_number IN ('PL-123/2023', 'PEC-456/2023', 'PL-789/2023')
    )
    -- Insert votes
    INSERT INTO vote (politician_id, bill_id, bill_title, vote_date, vote_position, vote_result)
    SELECT
        lula_id,
        b.id,
        'Lei de Incentivo às Energias Renováveis',
        '2023-02-15',
        'sim',
        'aprovado'
    FROM bill_data b
    WHERE b.bill_number = 'PL-123/2023'
    ON CONFLICT (id) DO NOTHING;

    INSERT INTO vote (politician_id, bill_id, bill_title, vote_date, vote_position, vote_result)
    SELECT
        lula_id,
        b.id,
        'Reforma Orçamentária',
        '2023-03-20',
        'não',
        'aprovado'
    FROM bill_data b
    WHERE b.bill_number = 'PEC-456/2023'
    ON CONFLICT (id) DO NOTHING;

    INSERT INTO vote (politician_id, bill_id, bill_title, vote_date, vote_position, vote_result)
    SELECT
        lira_id,
        b.id,
        'Lei de Incentivo às Energias Renováveis',
        '2023-02-15',
        'não',
        'aprovado'
    FROM bill_data b
    WHERE b.bill_number = 'PL-123/2023'
    ON CONFLICT (id) DO NOTHING;

    -- Insert contributions
    INSERT INTO political_contribution (politician_id, contributor_name, contributor_type, amount, contribution_date)
    VALUES
        (lula_id, 'Federação Brasil da Esperança', 'Partido', 500000.00, '2023-01-05'),
        (lira_id, 'Associação Brasileira do Agronegócio', 'Associação', 750000.00, '2023-01-10'),
        (tebet_id, 'Confederação Nacional da Indústria', 'Grupo Industrial', 1000000.00, '2023-02-05')
    ON CONFLICT (id) DO NOTHING;
END $$;

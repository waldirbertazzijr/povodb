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

    -- Get bill IDs for votes

    -- Insert votes for Lula on PL-123/2023
    INSERT INTO vote (politician_id, bill_id, bill_title, vote_date, vote_position, vote_result)
    SELECT
        lula_id,
        id,
        'Lei de Incentivo às Energias Renováveis',
        DATE '2023-02-15',
        'sim',
        'aprovado'
    FROM bill
    WHERE bill_number = 'PL-123/2023'
    ON CONFLICT (id) DO NOTHING;

    -- Insert votes for Lula on PEC-456/2023
    INSERT INTO vote (politician_id, bill_id, bill_title, vote_date, vote_position, vote_result)
    SELECT
        lula_id,
        id,
        'Reforma Orçamentária',
        DATE '2023-03-20',
        'não',
        'aprovado'
    FROM bill
    WHERE bill_number = 'PEC-456/2023'
    ON CONFLICT (id) DO NOTHING;

    -- Insert votes for Lira on PL-123/2023
    INSERT INTO vote (politician_id, bill_id, bill_title, vote_date, vote_position, vote_result)
    SELECT
        lira_id,
        id,
        'Lei de Incentivo às Energias Renováveis',
        DATE '2023-02-15',
        'não',
        'aprovado'
    FROM bill
    WHERE bill_number = 'PL-123/2023'
    ON CONFLICT (id) DO NOTHING;

    -- Insert contributions
    INSERT INTO political_contribution (politician_id, contributor_name, contributor_type, amount, contribution_date)
    VALUES
        (lula_id, 'Federação Brasil da Esperança', 'Partido', 500000.00, DATE '2023-01-05'),
        (lira_id, 'Associação Brasileira do Agronegócio', 'Associação', 750000.00, DATE '2023-01-10'),
        (tebet_id, 'Confederação Nacional da Indústria', 'Grupo Industrial', 1000000.00, DATE '2023-02-05')
    ON CONFLICT (id) DO NOTHING;
END $$;

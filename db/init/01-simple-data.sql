-- Simple sample data initialization
-- Just create a few politicians to get started

-- Insert sample politicians
INSERT INTO politician (name, party, position, country, state_province, bio)
VALUES
    ('Luiz Inácio Lula da Silva', 'PT', 'Presidente', 'Brasil', 'São Paulo', 'Ex-metalúrgico e líder sindical, foi presidente do Brasil por dois mandatos (2003-2010) e eleito novamente em 2022.'),
    ('Arthur Lira', 'PP', 'Presidente da Câmara', 'Brasil', 'Alagoas', 'Deputado Federal desde 2011, eleito presidente da Câmara dos Deputados em 2021 e reeleito em 2023.'),
    ('Simone Tebet', 'MDB', 'Ministra', 'Brasil', 'Mato Grosso do Sul', 'Ex-senadora e atual Ministra do Planejamento, foi a terceira colocada na eleição presidencial de 2022.')
ON CONFLICT (id) DO NOTHING;

-- Insert a simple bill
INSERT INTO bill (bill_number, title, description, introduced_date, status)
VALUES
    ('PL-123/2023', 'Lei de Incentivo às Energias Renováveis', 'Projeto de lei que promove o desenvolvimento e infraestrutura de energia renovável no Brasil', DATE '2023-01-15', 'Em Comissão')
ON CONFLICT (id) DO NOTHING;

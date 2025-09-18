# PovoDB - Plataforma de Transparência Política

Uma aplicação moderna full-stack para acompanhamento de dados políticos, incluindo políticos, projetos de lei, votações e contribuições de campanha.

## Visão Geral do Projeto

PovoDB é um boilerplate para construir aplicações de transparência política brasileira, fornecendo uma base sólida com:

- **Backend**: Python + FastAPI + SQLAlchemy + Alembic
- **Frontend**: React + TypeScript + Shadcn/ui + Tailwind CSS
- **Database**: PostgreSQL
- **Reverse Proxy**: Nginx
- **Containerização**: Docker + Docker Compose

## Development URLs

- **Main App**: http://app.povodb.test
- **API**: http://api.povodb.test
- **Database**: db.povodb.test:5432

## Início Rápido

### Pré-requisitos

- Docker e Docker Compose
- Atualize seu arquivo hosts para incluir:
  ```
  127.0.0.1 app.povodb.test
  127.0.0.1 api.povodb.test
  127.0.0.1 db.povodb.test
  ```

### Executando a Aplicação

1. Clone o repositório
2. Inicie a aplicação:

```bash
cd povodb
docker-compose up
```

3. Acesse a aplicação:
   - Frontend: http://app.povodb.test
   - Documentação da API: http://api.povodb.test/api/v1/docs

## Project Structure

```
povodb/
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   └── alembic/
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
├── db/
│   ├── Dockerfile
│   └── init/
└── nginx/
    ├── Dockerfile
    └── nginx.conf
```

## Funcionalidades Principais

- **Backend FastAPI**:
  - Documentação OpenAPI automática
  - SQLAlchemy 2.0+ com suporte assíncrono
  - Alembic para migrações de banco de dados
  - CORS configurado corretamente

- **Frontend React**:
  - TypeScript para segurança de tipos
  - Componentes Shadcn/ui
  - Tailwind CSS para estilização
  - React Router para navegação
  - Axios para comunicação com API

- **Banco de Dados**:
  - PostgreSQL 15+ com esquemas adequados
  - Dados de exemplo de políticos brasileiros
  - Persistência de volume

- **Experiência de Desenvolvimento**:
  - Hot reload para frontend e backend
  - Ambiente de desenvolvimento containerizado
  - Redes configuradas corretamente entre serviços

## Endpoints da API

- `/api/v1/politicians` - Dados de políticos
- `/api/v1/bills` - Informações sobre projetos de lei
- `/api/v1/votes` - Registros de votações
- `/api/v1/contributions` - Contribuições de campanha
- `/api/v1/health` - Verificação de saúde da API

## Desenvolvimento

### Desenvolvimento Backend

- O backend roda em http://api.povodb.test
- A documentação da API está disponível em http://api.povodb.test/api/v1/docs
- As migrações do banco de dados são gerenciadas pelo Alembic

### Desenvolvimento Frontend

- O frontend roda em http://app.povodb.test
- Hot reload está habilitado para desenvolvimento em tempo real
- Os componentes usam Shadcn/ui com Tailwind CSS para estilização

## Troubleshooting

### Database Connection Issues

If you encounter database connection issues:

1. **Tables don't exist error**: 
   - This can happen if Alembic migrations didn't run correctly
   - Solution: Run `docker-compose exec backend python init_alembic.py` to manually run the migrations

2. **PostgreSQL driver error**:
   - If you see "asyncpg.exceptions.UndefinedTableError: relation does not exist"
   - Solution: Restart the backend service with `docker-compose restart backend`

3. **Connection refused**:
   - Ensure the database container is healthy: `docker-compose ps db`
   - Check the database logs: `docker-compose logs db`

### Frontend Issues

1. **Missing components**:
   - If you see errors about missing React components
   - Solution: Run `docker-compose exec frontend npm install` to reinstall dependencies

2. **Hot reload not working**:
   - Try accessing the frontend directly at http://localhost:3000
   - Check frontend logs: `docker-compose logs frontend`

## License

MIT
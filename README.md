# App de Banco de Dados

Este projeto consiste em implementar um sistema web fullstack com opção de criar, editar, remover pessoas manualmente ou carregar um .csv com os dados.

## Tecnologias utilizadas

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: React, Bootstrap

## Requisitos

- Python 3.x
- Node.js
- NPM
- PostgreSQL

## Instalação

### Backend
Navegue até o diretório do projeto:
```
cd people-database/backend
```
Crie e ative um ambiente virtual:
```
python -m venv venv
source venv/bin/activate
```
Instale as dependências:
```
pip install -r requirements.txt
```
Crie as tabelas necessárias no Postgres:
```sql
CREATE TABLE people (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    birthdate DATE,
    gender VARCHAR(20),
    nationality VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    person_id INTEGER NOT NULL,
    operation_type VARCHAR(50) NOT NULL,
    old_data JSONB,
    new_data JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Frontend
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
Inicie o servidor:
```
uvicorn main:app --reload
```

### Frontend
Navegue até o diretório do frontend:
```
cd people-database/frontend
```
Instale as dependências:
```
npm install
```
Entre na pasta da aplicação e inicie o servidor de desenvolvimento:
```
cd people-app
npm start
```

## Documentação
O backend possui um swagger que pode ser acessado em http://localhost:8000/docs

O backend foi organizado de acordo com boas práticas de arquitetura limpa, com separação de responsabilidade.

* backend
    * models: define os modelos do banco de dados compatíveis com o SQLAlchemy
    * routers: gerencia as requisições HTTP e direciona para os controladores apropriados em /services
    * schemas: contém modelos do Pydantic que padronizam a entrada e saída de dados na API
    * services: contém as regras de negócio da aplicação

Como os dados do .csv parecem ser bem estruturados, um banco relacional é uma ótima escolha. O PostgreSQL foi escolhido devido à sua crescente popularidade na comunidade dev.

## Demonstração
[Vídeo de demonstração](https://www.youtube.com/watch?v=LLueMRGUgms)
# Banco Transfer API

API backend para simulação de transferências bancárias, desenvolvida com Python, FastAPI, SQLAlchemy e PostgreSQL.

O projeto tem como objetivo aplicar conceitos de desenvolvimento backend, modelagem de dados, transações no banco de dados, consistência de saldo e organização de uma API financeira.

> Projeto em desenvolvimento. Atualmente, a infraestrutura do banco de dados e a conexão da aplicação com o PostgreSQL estão configuradas.

## Tecnologias

- Python 3.14
- FastAPI
- SQLAlchemy
- PostgreSQL 18
- Psycopg
- Pydantic Settings
- Docker
- uv

## Estado atual

Até o momento, o projeto possui:

- PostgreSQL executado em contêiner Docker;
- configurações carregadas por variáveis de ambiente;
- conexão entre a aplicação e o banco de dados;
- modelos iniciais de usuários, transações e transferências;
- relacionamentos e restrições básicas de integridade.

A API ainda não possui endpoints disponíveis para utilização.

## Estrutura do projeto

```text
banco-transfer-api/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── database.py
│   └── __init__.py
├── .env.example
├── .gitignore
├── docker-compose.yaml
├── models.py
├── pyproject.toml
├── uv.lock
├── LICENSE
└── README.md
```

## Pré-requisitos

Antes de executar o projeto, instale:

- [Python 3.14 ou superior](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Configuração do ambiente

Clone o repositório:

```bash
git clone https://github.com/devNicolasAmaral/banco-transfer-api.git
cd banco-transfer-api
```

Crie o arquivo local de variáveis de ambiente a partir do exemplo.

No PowerShell:

```powershell
Copy-Item .env.example .env
```

Depois, abra o arquivo `.env` e defina os dados do PostgreSQL:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=defina_uma_senha
POSTGRES_DB=transfer_database
```

O arquivo `.env` contém configurações locais e não deve ser enviado ao GitHub.

## Instalação das dependências

Instale as dependências do projeto:

```bash
uv sync
```

## Inicialização do banco de dados

Com o Docker Desktop em execução, inicie o PostgreSQL:

```bash
docker compose up -d
```

Confira o estado do contêiner:

```bash
docker compose ps
```

Para interromper o contêiner:

```bash
docker compose stop
```

Para iniciá-lo novamente:

```bash
docker compose start
```

## Próximas etapas

- reorganizar os modelos dentro do pacote `app`;
- configurar sessões do SQLAlchemy;
- adicionar migrações com Alembic;
- revisar a modelagem das transferências;
- implementar regras de negócio;
- criar endpoints com FastAPI;
- adicionar validação e tratamento de erros;
- desenvolver testes automatizados;
- documentar os endpoints da API.

## Licença

Este projeto está licenciado conforme os termos disponíveis no arquivo [LICENSE](LICENSE).
# Banco Transfer API

API REST para simulação de transferências bancárias, desenvolvida com Python, FastAPI, SQLAlchemy e PostgreSQL.

O projeto tem como objetivo aplicar conceitos de desenvolvimento backend, modelagem de dados, transações atômicas, consistência de saldo e organização em camadas de uma API financeira.

> Projeto em desenvolvimento. A persistência de dados, as regras iniciais de negócio e os primeiros endpoints da API já estão implementados.

## Tecnologias

* Python 3.14
* FastAPI
* Pydantic
* pydantic-settings
* SQLAlchemy
* Alembic
* PostgreSQL 18
* psycopg2-binary
* Docker
* uv
* pytest

## Estado atual

Até o momento, o projeto possui:

* PostgreSQL em Docker, configurações por variáveis de ambiente e sessões com SQLAlchemy;
* modelos de contas, transferências e lançamentos, com relacionamentos e restrições de integridade;
* migrações versionadas com Alembic;
* schemas de entrada e saída validados com Pydantic;
* endpoints para cadastro e consulta de usuários;
* endpoint para transferências atômicas, com bloqueio de contas, validação de saldo e rollback automático;
* testes automatizados iniciais para validação dos schemas;
* documentação com OpenAPI e Swagger UI.

> Limitação atual: novas contas são criadas com saldo zero e ainda não existe uma operação para adicionar saldo pela API.

## Estrutura do projeto

```text
banco-transfer-api/
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── account_entry.py
│   │   ├── base.py
│   │   ├── enums.py
│   │   ├── transfer.py
│   │   └── user.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── transfer.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── account_entry.py
│   │   ├── transfer.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── exceptions.py
│   │   ├── transfer.py
│   │   └── user.py
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── schemas/
│       ├── test_transfer.py
│       └── test_user.py
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yaml
├── LICENSE
├── pyproject.toml
├── README.md
└── uv.lock
```

## Pré-requisitos

Antes de executar o projeto, instale:

* [Python 3.14 ou superior](https://www.python.org/)
* [uv](https://docs.astral.sh/uv/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)

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

## Aplicação das migrações

Crie ou atualize as tabelas do banco de dados:

```bash
uv run alembic upgrade head
```

Confira a migração atualmente aplicada:

```bash
uv run alembic current
```

## Execução da API

Inicie o servidor de desenvolvimento:

```bash
uv run uvicorn app.main:app --reload
```

Acesse a documentação interativa:

```text
http://127.0.0.1:8000/docs
```

## Execução dos testes

Execute os testes automatizados:

```bash
uv run pytest -q
```

## Gerenciamento do contêiner

Para interromper o PostgreSQL sem remover o contêiner:

```bash
docker compose stop
```

Para iniciá-lo novamente:

```bash
docker compose start
```

## Próximas etapas

* ampliar os testes unitários dos schemas;
* desenvolver testes de integração para serviços, endpoints, banco de dados e rollback;
* testar transferências concorrentes e a prevenção de saldo inconsistente;
* definir uma operação segura para adicionar saldo às contas;
* implementar idempotência para evitar transferências duplicadas;
* centralizar e padronizar o tratamento de exceções da API;
* criar endpoints para consulta de transferências e extrato das contas;
* configurar ferramentas de lint e verificação de tipos;
* adicionar uma pipeline de integração contínua;
* documentar os endpoints e exemplos de requisição no README.

## Licença

Este projeto está licenciado conforme os termos disponíveis no arquivo [LICENSE](LICENSE).

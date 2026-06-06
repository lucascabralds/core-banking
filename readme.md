# 🚀 Pismo Core-Banking Pro

API assíncrona de alta performance desenvolvida em Python para gerenciamento de contas, controle estrito de saldo e livro razão (*ledger*) imutável de transações financeiras.

Este projeto foi concebido elevando os requisitos originais do desafio técnico da Pismo para um nível de arquitetura sênior e pronta para produção, aplicando concorrência segura, idempotência e os princípios de **Clean Architecture** (Arquitetura Limpa).

---

## 🛠️ Stack Tecnológica

- **Linguagem:** Python 3.11+
- **Framework Web:** FastAPI (Totalmente assíncrono com Uvicorn)
- **ORM / Banco de Dados:** SQLAlchemy 2.0 (Async Engine) + driver `asyncpg`
- **Banco de Dados:** PostgreSQL 15 (Isolado via Docker)
- **Validação de Dados:** Pydantic v2
- **Ambiente:** Docker & Docker Compose

---

## 🏗️ Estrutura de Pastas e Visão de Arquitetura

O projeto adota os conceitos de **Clean/Hexagonal Architecture** para garantir que as regras de negócio fiquem 100% isoladas de detalhes técnicos, frameworks ou adaptadores externos.

```text
core-banking/
├── docker-compose.yml       # Infraestrutura local (Bancos de Produção e Testes)
├── requirements.txt         # Gerenciamento de dependências
├── User_History.md          # Especificação ágil e critérios de aceitação (BDD)
├── README.md                # Instruções e documentação do projeto
└── src/
    ├── __init__.py
    ├── main.py              # Ponto de entrada (Inicialização da API FastAPI)
    │
    ├── api/                 # Camada de Apresentação / Transporte (HTTP REST)
    │   ├── __init__.py
    │   ├── health.py        # Verificação de saúde da aplicação
    │   └── v1/
    │       ├── __init__.py
    │       ├── accounts.py  # Endpoints de criação e consulta de contas
    │       └── transactions.py # Endpoints de criação de transações
    │
    ├── domain/              # Regras de Negócio Puras (Entidades e Casos de Uso)
    │   ├── __init__.py
    │   ├── accounts.py      # Contratos e validações lógicas da conta
    │   └── transactions.py  # Regras de sinais de transação e validação de saldo
    │
    └── infra/               # Detalhes Técnicos e Integrações de Infraestrutura
        ├── __init__.py
        ├── database.py      # Configuração de Sessão Assíncrona do SQLAlchemy
        ├── models.py        # Mapeamento Declarativo das Tabelas do PostgreSQL
        └── repositories.py  # Padrão Repository para Queries SQL e For Update Locks
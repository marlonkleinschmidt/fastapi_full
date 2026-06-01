# FastAPI Full

Projeto de API REST completa desenvolvida com boas práticas de desenvolvimento, testes automatizados e containerização.

---

## 🚀 Tecnologias e Bibliotecas

### Framework e API

- **FastAPI** — framework web moderno e assíncrono para construção de APIs REST com tipagem automática e documentação via Swagger
- **Uvicorn** — servidor ASGI de alta performance utilizado para rodar a aplicação FastAPI
- **Pydantic** — validação e serialização de dados com tipagem Python; utilizado para definir schemas de entrada e saída da API
- **Pydantic Settings** — gerenciamento de configurações e variáveis de ambiente com suporte a arquivos `.env`

### Banco de Dados

- **SQLAlchemy (AsyncIO)** — ORM com suporte assíncrono para mapeamento objeto-relacional e construção de queries
- **Alembic** — ferramenta de migrations para versionamento e evolução do schema do banco de dados
- **PostgreSQL** — banco de dados relacional utilizado em produção
- **psycopg (binary)** — driver assíncrono de conexão Python com PostgreSQL
- **aiosqlite** — driver assíncrono SQLite utilizado nos testes locais

### Autenticação e Segurança

- **PyJWT** — geração e validação de tokens JWT (JSON Web Token) para autenticação stateless
- **pwdlib (Argon2)** — hashing seguro de senhas utilizando o algoritmo Argon2, vencedor do Password Hashing Competition

### Qualidade de Código

- **Ruff** — linter e formatter extremamente rápido para Python; substitui flake8, isort e black em um único tool
- **Typos** — verificador de erros de digitação no código fonte

### Testes

- **pytest** — framework principal de testes, responsável por coletar, executar e reportar os testes
- **pytest-asyncio** — plugin que permite escrever e executar testes assíncronos com `async/await` no pytest
- **pytest-cov** — plugin de cobertura de código; gera relatórios HTML mostrando quais linhas foram testadas
- **factory-boy** — biblioteca para criação de objetos de teste (factories); evita repetição de código ao criar dados falsos
- **freezegun** — congela o tempo durante os testes, permitindo simular datas e horários específicos sem depender do relógio real
- **testcontainers** — sobe containers Docker reais durante os testes; utilizado para criar um PostgreSQL isolado por sessão de teste

### Arquitetura de Testes

- **Fixture** — mecanismo do pytest para compartilhar configurações e objetos entre testes de forma declarativa e reutilizável
- **Session fixture** — fixture que gerencia o ciclo de vida da sessão assíncrona do banco de dados, criando e destruindo as tabelas a cada teste
- **Factory** — padrão utilizado com factory-boy para gerar instâncias de modelos (`User`, `Todo`) com dados automáticos via `Sequence` e `LazyAttribute`
- **Conftest** — arquivo central de configuração dos testes; define fixtures compartilhadas como `client`, `session`, `user`, `token` e `mock_db_time`
- **TestClient** — cliente HTTP do Starlette para simular requisições à API nos testes sem precisar de um servidor real rodando
- **Mock** — técnica usada com `mock_db_time` para interceptar eventos do SQLAlchemy e forçar valores de `created_at` durante os testes

### Infraestrutura e DevOps

- **Docker** — containerização da aplicação para garantir ambiente consistente entre desenvolvimento e produção
- **Docker Compose** — orquestração dos containers da aplicação e do banco de dados com healthcheck e rede interna
- **entrypoint.sh** — script shell que executa as migrations antes de subir a API no container
- **Poetry** — gerenciador de dependências e empacotamento Python com suporte a grupos de dependências (dev/prod)
- **Taskipy** — executor de tarefas definidas no `pyproject.toml`; simplifica comandos como `task test`, `task run` e `task lint`

---

## ⚙️ Comandos

```bash
task run      # inicia a aplicação em modo desenvolvimento
task test     # roda os testes com cobertura de código
task lint     # verifica o código com Ruff
task format   # formata o código com Ruff
```

## 🐳 Rodando com Docker

```bash
docker compose up --build
```

A API estará disponível em **http://localhost:8000/docs**

Creditos ao curso fastapi do zero @Dunossauro

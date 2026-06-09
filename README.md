# FastAPI Full

Projeto de API REST completa desenvolvida com boas práticas de desenvolvimento, testes automatizados e containerização.

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

## 💉 Injeção de Dependências e Annotations

O FastAPI utiliza um sistema nativo de **injeção de dependências** baseado em `Depends()`, que resolve automaticamente os parâmetros das funções no momento da requisição. Combinado com o `Annotated` do Python, o código fica mais legível e reutilizável.

### Como funciona

Em vez de instanciar objetos manualmente dentro de cada endpoint, você declara o que precisa como parâmetro — o FastAPI resolve e injeta automaticamente.

```python
# Sem injeção — repetitivo e acoplado
@router.get('/users')
async def list_users():
    session = AsyncSession(engine)   # instanciado manualmente
    current_user = await get_user()  # chamado manualmente
    ...
```

```python
# Com injeção — limpo e desacoplado
@router.get('/users')
async def list_users(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    ...
```

### Annotated — centralizando as dependências

O `Annotated` permite nomear e reutilizar uma dependência em vários endpoints sem repetir o `Depends()` toda vez:

```python
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Define uma vez
SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

# Usa em qualquer router
@router.get('/todos')
async def list_todos(session: SessionDep, user: CurrentUser):
    ...

@router.post('/todos')
async def create_todo(session: SessionDep, user: CurrentUser, todo: TodoSchema):
    ...
```

Sem o `Annotated`, cada endpoint precisaria repetir `session: AsyncSession = Depends(get_session)` — verboso e propenso a inconsistências.

### Dependências utilizadas no projeto

| Alias         | Tipo resolvido              | Função                              |
| ------------- | --------------------------- | ----------------------------------- |
| `SessionDep`  | `AsyncSession`              | Sessão assíncrona do banco de dados |
| `CurrentUser` | `User`                      | Usuário autenticado via token JWT   |
| `OAuth2Form`  | `OAuth2PasswordRequestForm` | Formulário de login (email + senha) |

### Fluxo de uma requisição autenticada

```
Requisição HTTP
      ↓
OAuth2PasswordBearer     → extrai o token do header Authorization
      ↓
get_current_user()       → decodifica o JWT e busca o usuário no banco
      ↓
CurrentUser              → injeta o User já validado no endpoint
      ↓
Lógica do endpoint       → executa com sessão e usuário prontos
```

---

## 🔄 CI/CD com GitHub Actions

O projeto utiliza **GitHub Actions** para automatizar a execução dos testes a cada `push` ou `pull request` na branch `main`. O pipeline é definido pelo arquivo `.github/workflows/pipeline.yaml`.

### O que é GitHub Actions

É a plataforma de CI/CD nativa do GitHub. A cada evento (push, PR, tag), ela sobe um ambiente limpo, instala as dependências e executa os passos definidos no arquivo `.yaml` — garantindo que o código novo não quebra o que já existia.

### Estrutura do arquivo `.github/workflows/pipeline.yaml`
```
name: Pipeline

on:
push:
branches: ["main"]
pull_request:
branches: ["main"]

jobs:
test:
runs-on: ubuntu-latest

    steps:
      - name: Checkout do código
        uses: actions/checkout@v4

      - name: Instalar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Instalar Poetry
        run: pipx install poetry

      - name: Instalar dependências
        run: poetry install

      - name: Rodar testes
        run: poetry run task test
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          SECRET_KEY: ${{ secrets.SECRET_KEY }}
          ALGORITHM: ${{ secrets.ALGORITHM }}
          ACCESS_TOKEN_EXPIRE_MINUTES: ${{ secrets.ACCESS_TOKEN_EXPIRE_MINUTES }}
```
### O que cada bloco faz

- **`on`** — define quando o pipeline dispara; neste caso em todo push ou PR na `main`
- **`runs-on`** — define o sistema operacional do ambiente de execução (`ubuntu-latest`)
- **`actions/checkout@v4`** — clona o repositório no ambiente da Action
- **`actions/setup-python@v5`** — instala a versão correta do Python
- **`pipx install poetry`** — instala o Poetry para gerenciar as dependências
- **`poetry install`** — instala todas as dependências do projeto
- **`poetry run task test`** — executa os testes com cobertura de código
- **`env`** — injeta as variáveis de ambiente a partir dos secrets cadastrados no GitHub

### Cadastrando os secrets no GitHub

As variáveis do `.env` não podem ser expostas no código. Para disponibilizá-las na Action, cadastre-as como secrets:

```bash
gh secret set -f .env
```

Esse comando lê o arquivo `.env` local e cadastra cada variável em **Settings → Secrets → Actions** do repositório, de forma criptografada. A Action acessa via `${{ secrets.NOME_DA_VARIAVEL }}`.

---

## ⚙️ Comandos

```
task run      # inicia a aplicação em modo desenvolvimento
task test     # roda os testes com cobertura de código
task lint     # verifica o código com Ruff
task format   # formata o código com Ruff
```

## 🐳 Rodando com Docker

```
docker compose up --build
```

A API estará disponível em http://localhost:8000/docs

Creditos ao curso fastapi do zero @Dunossauro

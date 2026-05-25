# WsWorkApi — Cars API

API REST para gestão de veículos, marcas, modelos e usuários. Desenvolvida com FastAPI, SQLAlchemy 2.0 e PostgreSQL, com autenticação JWT e arquitetura em camadas.

---

## Stack

| Tecnologia | Uso |
|---|---|
| Python 3.12 | Linguagem |
| FastAPI | Framework HTTP |
| SQLAlchemy 2.0 | ORM |
| PostgreSQL | Banco de dados |
| Alembic | Migrations |
| Pydantic v2 | Validação e schemas |
| JWT (PyJWT) | Autenticação |
| Passlib + bcrypt | Hash de senhas |
| Poetry | Gerenciamento de dependências |
| Docker + Compose | Containerização |

---

## Arquitetura

```
app/
├── core/           # Config, segurança, JWT, dependencies
├── database/       # Engine, SessionLocal, tipos UUID
├── models/         # Entidades SQLAlchemy
├── schemas/        # Schemas Pydantic (request/response)
├── repositories/   # Acesso ao banco de dados
├── services/       # Regras de negócio
├── routes/         # Endpoints HTTP
└── main.py         # Factory da aplicação FastAPI
```

**Fluxo de uma requisição:**

```
Route → Service → Repository → Database
         ↓
       Schema (response)
```

- **Routes** — recebem HTTP, validam entrada, retornam responses tipadas
- **Services** — regras de negócio, erros HTTP, ownership
- **Repositories** — queries SQLAlchemy, paginação, soft delete
- **Models** — mapeamento ORM com UUID, timestamps e `deleted_at`

---

## Como rodar

### Pré-requisitos

- Python 3.12+
- Poetry
- PostgreSQL 16+ (local ou via Docker)

### 1. Clonar e configurar ambiente

```bash
git clone <repo-url>
cd WsWorkApi

cp .env.example .env
# Edite .env com suas credenciais
```

### 2. Instalar dependências

```bash
poetry install --no-root
```

### 3. Subir o banco (opcional — via Docker)

```bash
docker compose up db -d
```

### 4. Aplicar migrations

```bash
poetry run alembic upgrade head
```

### 5. Iniciar a API

```bash
poetry run uvicorn app.main:app --reload
```

A API estará disponível em **http://localhost:8000**

---

## Migrations

Gerenciadas com Alembic. A URL do banco é lida do `.env` via `app.core.config`.

```bash
# Aplicar todas as migrations
poetry run alembic upgrade head

# Criar nova migration (autogenerate)
poetry run alembic revision --autogenerate -m "descricao"

# Reverter última migration
poetry run alembic downgrade -1

# Ver histórico
poetry run alembic history

# Ver versão atual
poetry run alembic current
```

No Docker, as migrations rodam automaticamente ao iniciar o container (`entrypoint.sh`).

---

## Autenticação JWT

### Fluxo

1. **Registrar** — `POST /auth/register`
2. **Login** — `POST /auth/login` → retorna `access_token`
3. **Usar token** — header `Authorization: Bearer <token>`
4. **Perfil** — `GET /auth/me`

### Variáveis

| Variável | Descrição | Padrão |
|---|---|---|
| `JWT_SECRET` | Chave de assinatura | `change-me` |
| `JWT_ALGORITHM` | Algoritmo | `HS256` |
| `JWT_EXPIRE_MINUTES` | Expiração do token | `60` |

> Use um `JWT_SECRET` com pelo menos 32 caracteres em produção.

### Proteção de rotas

Todas as rotas CRUD exigem JWT. Exceções públicas: `/auth/register`, `/auth/login`, `/catalog/models`, `/health`.

### Ownership de carros

- Criação associa automaticamente o usuário autenticado
- Apenas o dono pode atualizar ou excluir seus carros (`403 Forbidden`)

---

## Endpoints

### Auth

| Método | Rota | Auth | Descrição |
|---|---|---|---|
| POST | `/auth/register` | Não | Registrar usuário |
| POST | `/auth/login` | Não | Login (retorna JWT) |
| GET | `/auth/me` | Sim | Usuário autenticado |

### Usuários

| Método | Rota | Descrição |
|---|---|---|
| GET | `/usuarios` | Listar (paginado) |
| GET | `/usuarios/{id}` | Obter por ID |
| POST | `/usuarios` | Criar |
| PATCH | `/usuarios/{id}` | Atualizar |
| DELETE | `/usuarios/{id}` | Soft delete |

### Marcas

| Método | Rota | Descrição |
|---|---|---|
| GET | `/marcas` | Listar (paginado) |
| GET | `/marcas/{id}` | Obter por ID |
| POST | `/marcas` | Criar |
| PATCH | `/marcas/{id}` | Atualizar |
| DELETE | `/marcas/{id}` | Soft delete |

### Modelos

| Método | Rota | Descrição |
|---|---|---|
| GET | `/modelos` | Listar (paginado) |
| GET | `/modelos/{id}` | Obter por ID |
| POST | `/modelos` | Criar |
| PATCH | `/modelos/{id}` | Atualizar |
| DELETE | `/modelos/{id}` | Soft delete |

### Carros

| Método | Rota | Descrição |
|---|---|---|
| GET | `/carros` | Listar com filtros |
| GET | `/carros/{id}` | Obter por ID |
| POST | `/carros` | Criar (dono = usuário logado) |
| PATCH | `/carros/{id}` | Atualizar (somente dono) |
| DELETE | `/carros/{id}` | Soft delete (somente dono) |

**Filtros de listagem (`GET /carros`):**

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `marca` | UUID | Filtrar por marca |
| `modelo` | UUID | Filtrar por modelo |
| `ano` | int | Filtrar por ano |
| `combustivel` | enum | FLEX, GASOLINA, DIESEL, ELETRICO, HIBRIDO |
| `page` | int | Página (padrão: 1) |
| `page_size` | int | Itens por página (padrão: 20, máx: 100) |

### Catálogo

| Método | Rota | Auth | Descrição |
|---|---|---|---|
| GET | `/catalog/models` | Não | Lista modelos com marca e valor FIPE |

### Health

| Método | Rota | Descrição |
|---|---|---|
| GET | `/health` | Health check |

---

## Swagger

Documentação interativa disponível em:

| URL | Descrição |
|---|---|
| http://localhost:8000/docs | Swagger UI |
| http://localhost:8000/redoc | ReDoc |
| http://localhost:8000/openapi.json | Schema OpenAPI |

### Como autenticar no Swagger

1. Faça login em `POST /auth/login`
2. Copie o `access_token` da resposta
3. Clique em **Authorize** (cadeado no topo)
4. Informe: `Bearer <seu_token>`
5. Teste os endpoints protegidos

---

## Docker

### Subir tudo (API + PostgreSQL)

```bash
cp .env.example .env
docker compose up --build
```

Serviços:

| Serviço | URL / Porta |
|---|---|
| API | http://localhost:8000 |
| PostgreSQL | localhost:5432 |

### Hot reload

O container `api` monta o código local como volume e inicia o Uvicorn com `--reload`. Alterações em `app/` e `alembic/` são refletidas automaticamente.

### Variáveis no Docker

O `docker-compose.yml` sobrescreve `DATABASE_URL` para apontar ao serviço `db`:

```
postgresql://postgres:postgres@db:5432/wsworkapi
```

Demais variáveis vêm do arquivo `.env`.

### Comandos úteis

```bash
# Subir em background
docker compose up -d --build

# Ver logs
docker compose logs -f api

# Parar
docker compose down

# Parar e remover volumes (apaga dados do banco)
docker compose down -v

# Rodar migration manualmente no container
docker compose exec api alembic upgrade head
```

### Produção

Para produção, remova `--reload` do `entrypoint.sh` e considere:

- `JWT_SECRET` forte e único
- `DEBUG=false`
- Reverse proxy (Nginx / Traefik)
- Secrets manager para credenciais

---

## Variáveis de ambiente

| Variável | Obrigatória | Descrição |
|---|---|---|
| `DATABASE_URL` | Sim | URL de conexão PostgreSQL |
| `JWT_SECRET` | Sim | Chave secreta JWT |
| `JWT_ALGORITHM` | Não | Algoritmo JWT (padrão: HS256) |
| `JWT_EXPIRE_MINUTES` | Não | Expiração do token em minutos |
| `APP_NAME` | Não | Nome exibido na API |
| `APP_VERSION` | Não | Versão da API |
| `DEBUG` | Não | Modo debug |

---

## Licença

Projeto privado — WsWorkApi.

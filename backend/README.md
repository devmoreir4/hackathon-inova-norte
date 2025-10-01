# Sicoob Fluminense API

API para engajamento comunitário e desenvolvimento sustentável do Sicoob Fluminense.

## Funcionalidades

- **Gestão de Cooperados** - CRUD completo de cooperados
- **Projetos de Impacto Social** - Sistema de proposta e votação
- **Eventos Comunitários** - Calendário de eventos e feiras
- **Fórum de Discussões** - Espaço para troca de conhecimento
- **Chatbot IA** - Educação financeira e suporte

## Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **SQLite** - Banco de dados (desenvolvimento)
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI

## Estrutura do Projeto

```
backend/
├── app/
│   ├── domain/           # Modelos de domínio e lógica de negócio
│   │   └── models.py
│   ├── application/      # Casos de uso, DTOs e exceções
│   │   └── dto.py
│   ├── infrastructure/   # Banco de dados e APIs externas
│   │   └── database.py
│   └── interface/        # Camada web: rotas FastAPI
│       ├── main.py
│       ├── routes.py
│       └── user_routes.py
├── tests/               # Testes unitários e de integração
├── requirements.txt     # Dependências Python
├── run.py              # Ponto de entrada da aplicação
└── README.md           # Este arquivo
```

## Como Executar

### 1. Configurar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
venv\Scripts\activate

# Ativar ambiente virtual (Linux/Mac)
source venv/bin/activate
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Executar a Aplicação

```bash
# Desenvolvimento (com reload automático)
python run.py

# Ou usando uvicorn diretamente
uvicorn app.interface.main:app --reload --host 0.0.0.0 --port 5000
```

### 4. Acessar a API

- **API**: http://localhost:5000
- **Documentação Swagger**: http://localhost:5000/docs
- **Documentação ReDoc**: http://localhost:5000/redoc
- **Health Check**: http://localhost:5000/health

## Endpoints Principais

### Cooperados
- `GET /api/v1/users/` - Listar cooperados
- `POST /api/v1/users/` - Criar cooperado
- `GET /api/v1/users/{id}` - Buscar cooperado por ID
- `PUT /api/v1/users/{id}` - Atualizar cooperado
- `DELETE /api/v1/users/{id}` - Desativar cooperado
- `GET /api/v1/users/email/{email}` - Buscar por email

### Health Check
- `GET /health` - Status básico da API
- `GET /health/detailed` - Status detalhado com informações do sistema

### Modelos Principais

- **User** - Cooperados
- **Project** - Projetos de impacto social
- **Vote** - Votos em projetos
- **Event** - Eventos comunitários
- **EventRegistration** - Inscrições em eventos

## Desenvolvimento

### Adicionar Novas Rotas

1. Criar arquivo de rotas em `app/interface/`
2. Importar e incluir no `routes.py`
3. Adicionar DTOs em `app/application/dto.py`
4. Atualizar modelos em `app/domain/models.py`

### Estrutura DDD

O projeto segue os princípios de Domain-Driven Design (DDD):

- **Domain**: Modelos de negócio e regras
- **Application**: Casos de uso e DTOs
- **Infrastructure**: Banco de dados e serviços externos
- **Interface**: Controllers e rotas da API

# Hackathon Inova Norte

## Como Executar Backend

### 1. Pré-requisitos

- Ter o [Python](https://www.python.org/downloads/) instalado e configurado no seu ambiente.

### 2. Configurar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
venv\Scripts\activate

# Ativar ambiente virtual (Linux/Mac)
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a Aplicação

```bash
# Desenvolvimento (com reload automático)
python run.py

# Ou usando uvicorn diretamente
uvicorn app.interface:app --reload --host 0.0.0.0 --port 5000
```

### 5. Acessar a API

- **API**: http://localhost:5000
- **Documentação Swagger**: http://localhost:5000/docs
- **Documentação ReDoc**: http://localhost:5000/redoc
- **Health Check**: http://localhost:5000/health

## Como Executar Frontend

### 1. Pré-requisitos

- Ter o [Flutter](https://flutter.dev/docs/get-started/install) instalado e configurado no seu ambiente.

### 2. Instalar Dependências

```bash
# Navegar para a pasta do frontend
cd frontend

# Instalar as dependências
flutter pub get
```

### 3. Executar a Aplicação

```bash
# Executar o aplicativo
flutter run
```

## Testes do Backend

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=app

# Executar testes específicos
pytest tests/test_users.py -v
```

## Reset do Banco de Dados

```bash
python reset_db.py
```

## Popular Banco de Dados
```bash
python init_db.py
```

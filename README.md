# hackathon-inova-norte

## Como Executar Backend

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
uvicorn app.interface:app --reload --host 0.0.0.0 --port 5000
```

### 4. Acessar a API

- **API**: http://localhost:5000
- **Documentação Swagger**: http://localhost:5000/docs
- **Documentação ReDoc**: http://localhost:5000/redoc
- **Health Check**: http://localhost:5000/health

## Testes

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

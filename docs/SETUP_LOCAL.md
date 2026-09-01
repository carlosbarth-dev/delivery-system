# 🚀 Setup Local - Como Rodar MVP v0.1.0

Guia passo-a-passo para rodar o projeto na sua máquina.

---

## 📋 Prerequisitos

- Python 3.9+ instalado
- Node.js 16+ instalado (npm ou yarn)
- Git instalado
- Editor (VS Code recomendado)
- ~2GB de espaço livre

---

## 🔧 Instalação Backend

### 1. Clonar repositório

```bash
git clone https://github.com/carlosbarth-dev/delivery-system.git
cd delivery-system/backend
```

### 2. Criar ambiente virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

Expected output:
```
Successfully installed fastapi==0.104.0 sqlalchemy==2.0.23 pydantic==2.5.0 pytest==7.4.3
```

### 4. Criar `.env`

Copie `.env.example` para `.env`:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Edite `.env`:
```
DATABASE_URL=sqlite:///./delivery.db
DEBUG=True
SECRET_KEY=dev-secret-change-me
```

### 5. Inicializar banco de dados

```bash
python -c "from app.config import init_db; init_db()"
```

Esperado: Database criado em `backend/delivery.db`

### 6. Popular com dados de teste (opcional)

```bash
python -c "from app.utils.db import seed_products; seed_products()"
```

### 7. Rodar servidor

```bash
uvicorn main:app --reload --port 8000
```

Output esperado:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

**Verificar se está OK:**
```
curl http://localhost:8000/healthcheck
# Resposta: {"status":"healthy","database":"connected"}
```

---

## 🎨 Instalação Frontend

### 1. Navegar para frontend

**Mantenha o backend rodando em outro terminal!**

```bash
cd ../frontend
```

### 2. Instalar dependências

```bash
npm install
```

### 3. Criar `.env`

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Edite `.env`:
```
VITE_API_URL=http://localhost:8000
```

### 4. Rodar desenvolvimento

```bash
npm run dev
```

Output esperado:
```
  VITE v5.0.0  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

**Abra navegador:** `http://localhost:5173`

---

## 🐳 Alternativa: Docker (Recomendado)

Se preferir isolar tudo:

### 1. Ter Docker instalado

[Download Docker Desktop](https://www.docker.com/products/docker-desktop)

### 2. Rodar com Docker Compose

```bash
# Na raiz do projeto
cd delivery-system
docker-compose up
```

Aguarde (~1-2 min primeira vez):
```
backend-1  | INFO:     Uvicorn running on http://0.0.0.0:8000
frontend-1 | ➜  Local:   http://localhost:5173/
```

**Parar:**
```
docker-compose down
```

---

## ✅ Testes

### Backend

```bash
cd backend

# Rodar todos os testes
pytest

# Rodar com cobertura
pytest --cov=app tests/

# Rodar testes específicos
pytest tests/test_products.py
pytest tests/test_orders.py
```

### Frontend

```bash
cd frontend

# Não há testes no MVP ainda
# Será adicionado em v0.2.0
```

---

## 🧪 Testar Endpoints (cURL)

### Produtos

```bash
# Listar produtos
curl http://localhost:8000/produtos

# Produto específico
curl http://localhost:8000/produtos/1

# Com filtro
curl "http://localhost:8000/produtos?search=pizza"
```

### Pedidos

```bash
# Criar pedido
curl -X POST http://localhost:8000/pedidos \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: test-123" \
  -d '{
    "email": "teste@example.com",
    "items": [
      {"product_id": 1, "quantity": 1, "price": 29.99}
    ],
    "total_price": 29.99
  }'

# Recuperar pedido (rastreamento)
curl "http://localhost:8000/pedidos/1?email=teste@example.com"
```

---

## 🐛 Troubleshooting

### Erro: "Port 8000 already in use"

```bash
# Encontre processo usando porta 8000
lsof -i :8000  # macOS/Linux

# Ou use porta diferente
uvicorn main:app --reload --port 8001
```

### Erro: "ModuleNotFoundError: No module named 'fastapi'"

```bash
# Certificar que venv está ativado
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate    # macOS/Linux

# Reinstalar dependências
pip install -r requirements.txt
```

### Erro: "Cannot find module 'vue'"

```bash
# Reinstalar node_modules
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### Database corrompido

```bash
# Deletar e recriar
cd backend
rm delivery.db
python -c "from app.config import init_db; init_db()"
python -c "from app.utils.db import seed_products; seed_products()"
```

### API não responde no Frontend

Verificar `.env` do frontend:
```
VITE_API_URL=http://localhost:8000  # ← Correto?
```

---

## 📊 Estrutura de Pastas Esperada

Após setup:

```
delivery-system/
├── backend/
│   ├── venv/                    # ← Ambiente virtual
│   ├── app/                     # ← Código
│   ├── tests/                   # ← Testes
│   ├── delivery.db              # ← Database SQLite (criado automaticamente)
│   ├── .env                     # ← Configuração local
│   ├── requirements.txt
│   └── main.py
│
├── frontend/
│   ├── node_modules/            # ← Dependências Node (criadas por npm install)
│   ├── src/                     # ← Código
│   ├── .env                     # ← Configuração local
│   ├── package.json
│   └── vite.config.js
│
└── docs/                        # ← Documentação
```

---

## 🔗 Endpoints Úteis

### Development

| Recurso | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger (API Docs) | http://localhost:8000/docs |
| ReDoc (API Docs) | http://localhost:8000/redoc |

---

## 📝 Próximas Etapas

1. ✅ Backend rodando
2. ✅ Frontend rodando
3. ⏳ Crie uma branch: `git checkout -b feature/seu-nome`
4. ⏳ Escolha uma tarefa em [TAREFAS_DISPONIVEIS.md](./TAREFAS_DISPONIVEIS.md)
5. ⏳ Faça commit e PR para `dev`

---

## 🎓 Dicas Úteis

### Hot Reload
- Backend: Automático com `--reload`
- Frontend: Automático com Vite

### Debug
```python
# Backend: adicione em qualquer lugar
from app.config import db
db.session.query(Product).all()  # Ver dados

# Frontend: abra DevTools (F12)
console.log(store.carrinho)  # Ver estado Pinia
```

### Limpar tudo

```bash
# Backend
cd backend
rm -rf venv delivery.db

# Frontend
cd frontend
rm -rf node_modules .dist

# Recomeçar do zero
```

---

## 🆘 Precisa de ajuda?

1. Leia [ARQUITETURA.md](./ARQUITETURA.md)
2. Abra uma issue no GitHub
3. Converse com o Tech Lead

---

**Última atualização:** 2026-09-01

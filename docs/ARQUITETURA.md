# 🏗️ Arquitetura - Sistema de Delivery v0.1.0

Design técnico completo do projeto. Leia isto antes de codificar.

---

## 📐 Visão Geral

```
┌─────────────────────────────────────────────────────────────┐
│                   CLIENTE (Navegador)                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Vue.js Application                     │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │   │
│  │  │Products  │→ │Cart View │→ │OrderConfirmation│  │   │
│  │  │View      │  │(Pinia)   │  │(Pedido)         │  │   │
│  │  └────┬─────┘  └────┬─────┘  └────────┬─────────┘  │   │
│  │       │              │                │             │   │
│  │       └──────────────┼────────────────┘             │   │
│  │                      ↓                               │   │
│  │        ┌─────────────────────────┐                 │   │
│  │        │   localStorage (Cache)  │                 │   │
│  │        │   - carrinho            │                 │   │
│  │        │   - order_id (após POST)│                 │   │
│  │        └─────────────────────────┘                 │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     │ (Axios HTTP)                         │
│                     │ JSON Requests                        │
└─────────────────────┼──────────────────────────────────────┘
                      │
          ┌───────────┼───────────┐
          │           │           │
          v           v           v
    GET /produtos  POST /pedidos  GET /pedidos/{id}
          │           │           │
          └───────────┼───────────┘
                      │
        ┌─────────────────────────┐
        │   FastAPI Backend       │
        │                         │
        │  ┌──────────────────┐   │
        │  │ Routes:          │   │
        │  │ - products.py    │   │  (Respostas JSON)
        │  │ - orders.py      │   │
        │  └────────┬─────────┘   │
        │           │             │
        │  ┌────────v──────────┐  │
        │  │  Middleware:      │  │
        │  │ - Error Handler   │  │  (Tratamento global)
        │  │ - Idempotency     │  │
        │  └────────┬──────────┘  │
        │           │             │
        │  ┌────────v──────────┐  │
        │  │  Models:          │  │
        │  │ - Product         │  │  (SQLAlchemy ORM)
        │  │ - Order           │  │
        │  │ - User (vazio)    │  │
        │  └────────┬──────────┘  │
        │           │             │
        │  ┌────────v──────────┐  │
        │  │  Database Layer:  │  │
        │  │  config.py        │  │  (Conexão)
        │  └────────┬──────────┘  │
        │           │             │
        └───────────┼─────────────┘
                    │
        ┌───────────v──────────┐
        │   SQLite DB          │
        │ (MVP - arquivo local)│
        │                      │
        │  Table: products     │
        │  Table: orders       │
        │  Table: order_items  │
        └──────────────────────┘
```

---

## 🗂️ Estrutura de Pastas Explicada

```
backend/
├── app/
│   ├── __init__.py                      # Factory function create_app()
│   │                                      # Retorna app FastAPI configurada
│   │
│   ├── config.py                        # Variáveis ambiente + database engine
│   │   └─ DATABASE_URL (SQLite)
│   │   └─ DEBUG mode
│   │   └─ SQLAlchemy session factory
│   │
│   ├── models/                          # ORM Models (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── product.py                   # Tabela: products
│   │   │   └─ id, name, price, description, created_at
│   │   ├── order.py                     # Tabela: orders + order_items
│   │   │   └─ id, email, status, total_price, created_at
│   │   └── user.py                      # Tabela: users (vazio, pronto v0.2.0)
│   │
│   ├── schemas/                         # Pydantic Schemas (validação)
│   │   ├── __init__.py
│   │   ├── product_schema.py            # ProductSchema (GET), ProductCreateSchema
│   │   │   └─ Validar nome, preço > 0
│   │   └── order_schema.py              # OrderSchema, OrderCreateSchema
│   │       └─ Validar email, items[] não vazio
│   │
│   ├── routes/                          # Endpoints HTTP
│   │   ├── __init__.py
│   │   ├── products.py                  # GET /produtos, GET /produtos/{id}
│   │   │   └─ Filtros: name, price_range, etc
│   │   └── orders.py                    # POST /pedidos, GET /pedidos/{id}
│   │       └─ Gerar Idempotency-Key
│   │
│   ├── middleware/                      # Tratamento cross-cutting
│   │   ├── __init__.py
│   │   ├── error_handler.py             # Middleware global try-catch
│   │   │   └─ Retorna JSON estruturado em caso de erro
│   │   └── idempotency.py               # Cache de requisições duplicadas
│   │       └─ Hash dos dados + timestamp
│   │
│   └── utils/                           # Funções auxiliares
│       ├── __init__.py
│       └── db.py                        # Helpers de database (seed, etc)
│
├── tests/
│   ├── __init__.py
│   ├── test_products.py                 # Testes unitários produtos
│   └── test_orders.py                   # Testes unitários pedidos
│
├── requirements.txt                     # fastapi, sqlalchemy, pydantic, pytest
├── .env.example                         # Modelo de variáveis
├── main.py                              # Entry point (uvicorn)
├── Dockerfile                           # Build imagem Docker
└── docker-compose.yml                   # Orquestração (backend + frontend)

frontend/
├── src/
│   ├── main.js                          # Entry Vue.js
│   ├── App.vue                          # Root component
│   │
│   ├── views/                           # Páginas
│   │   ├── Products.vue                 # Catálogo + carrinho (side panel)
│   │   ├── Cart.vue                     # Revisão detalhada
│   │   └── OrderConfirmation.vue        # Confirmação + rastreamento
│   │
│   ├── api/
│   │   ├── client.js                    # Axios instance (base URL, headers)
│   │   │   └─ Interceptor para carregar token (v0.2.0)
│   │   └── endpoints.js                 # Funções exportadas
│   │       └─ getProducts(), createOrder(), etc
│   │
│   ├── store/
│   │   └── store.js                     # Pinia store (state + actions)
│   │       ├─ State: { carrinho: [], produtos: [], loading: false }
│   │       ├─ Actions: addToCart, removeFromCart, checkoutOrder
│   │       └─ Getters: totalPrice, itemCount
│   │
│   ├── components/                      # Componentes reutilizáveis
│   │   ├── ProductCard.vue              # Card de produto (imagem, nome, preço)
│   │   ├── LoadingSpinner.vue           # Spinner durante requisições
│   │   └── ErrorModal.vue               # Modal de erro + retry
│   │
│   └── styles/
│       └── main.css                     # CSS global (Tailwind setup)
│
├── public/
│   └── index.html
├── .env.example                         # VITE_API_URL = http://localhost:8000
├── package.json                         # vue, pinia, axios, vite
└── Dockerfile                           # Build imagem Vue.js

docs/
├── README.md                            # Index de documentação (este)
├── DECISOES.md                          # Decisões arquiteturais tomadas
├── DISCUSSOES_ABERTAS.md                # O que ainda deve ser discutido
├── TAREFAS_DISPONIVEIS.md               # Trabalhos por fazer (por área)
├── ROADMAP.md                           # Versões futuras (v0.2.0, v0.3.0)
├── ARQUITETURA.md                       # Este arquivo
├── API.md                               # Especificação endpoints
├── SETUP_LOCAL.md                       # Como rodar localmente
├── CONTRIBUINDO.md                      # Guia para novos devs
├── INCREMENTO_1_PLAN.md                 # Plano autenticação v0.2.0
└── BD_SETUP.md                          # Instruções MySQL para responsável
```

---

## 🔄 Fluxo de Dados: Pedido Anônimo (Caminho Feliz)

```
1. CLIENTE ABRE APLICAÇÃO
   └─ Frontend carrega produtos via GET /produtos
   └─ Salva em Pinia store
   └─ Exibe ProductCard para cada item

2. CLIENTE ADICIONA AO CARRINHO
   └─ Action em Pinia: addToCart(productId, quantity)
   └─ Estado atualiza: store.carrinho.push({productId, quantity, price})
   └─ localStorage.setItem("carrinho", JSON.stringify(store.carrinho))

3. CLIENTE VAI PARA CHECKOUT
   └─ View OrderConfirmation.vue
   └─ Usuário preenche email
   └─ Frontend gera: Idempotency-Key = hash(carrinho + timestamp)

4. CLIENTE SUBMITA PEDIDO
   └─ POST /pedidos com:
      {
        "email": "cliente@example.com",
        "items": [
          {"product_id": 1, "quantity": 2, "price": 10.99}
        ],
        "total_price": 21.98
      }
   └─ Header: Idempotency-Key: "abc123xyz"

5. BACKEND RECEBE
   └─ Middleware idempotency.py: verifica se key já existe
   └─ Se SIM → retorna pedido antigo (sem duplicar)
   └─ Se NÃO → continua
   └─ Valida com OrderCreateSchema (Pydantic)
   └─ Cria novo Order + OrderItems no BD
   └─ Salva Idempotency-Key no cache

6. BACKEND RESPONDE
   └─ Status 201 Created
      {
        "order_id": 42,
        "tracking_code": "PED-42-ABC123",
        "email": "cliente@example.com",
        "status": "pending",
        "created_at": "2026-09-01T10:30:00"
      }

7. CLIENTE RECEBE
   └─ Frontend exibe: "Pedido criado! Acompanhe em:"
   └─ localStorage.setItem("order_id", 42)
   └─ Mostra link de rastreamento: /rastreamento?order_id=42&email=...
```

---

## 🛡️ Tratamento de Erros (Resiliência)

### Frontend

```javascript
// api/client.js setup
const client = axios.create({
  baseURL: process.env.VITE_API_URL
})

client.interceptors.response.use(
  response => response.data,
  error => {
    // Erro de rede/conexão
    if (!error.response) {
      // Mostrar modal de reconexão
      store.setError("Falha de conexão. Tentando novamente...")
      // Retry automático com backoff exponencial
      return retryWithBackoff(error.config)
    }
    
    // Erro do servidor
    store.setError(error.response.data.detail || "Erro desconhecido")
    throw error
  }
)
```

### Backend

```python
# middleware/error_handler.py
@app.middleware("http")
async def error_handler_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # Log do erro (será melhorado em v0.2.0)
        print(f"❌ Erro: {str(e)}")
        
        # Retorna JSON estruturado
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
```

---

## 💾 Persistência & Storage

### Frontend (localStorage)

```javascript
// Carrinho persiste entre sessões
{
  "carrinho": [
    {"product_id": 1, "quantity": 2, "price": 10.99},
    {"product_id": 3, "quantity": 1, "price": 25.00}
  ],
  "order_id": 42,  // Após pedido bem-sucedido
  "timestamp": "2026-09-01T10:30:00"
}
```

### Backend (SQLite - MVP)

```
Arquivo: delivery.db (gerado automaticamente)

Tabelas:
├── products
│   ├─ id (Primary Key)
│   ├─ name (String)
│   ├─ price (Float)
│   ├─ description (Text)
│   └─ created_at (DateTime)
│
├── orders
│   ├─ id (Primary Key)
│   ├─ email (String)
│   ├─ status (Enum: pending, preparing, ready, completed)
│   ├─ total_price (Float)
│   ├─ created_at (DateTime)
│   └─ updated_at (DateTime)
│
└── order_items
    ├─ id (Primary Key)
    ├─ order_id (Foreign Key → orders.id)
    ├─ product_id (Foreign Key → products.id)
    ├─ quantity (Integer)
    └─ price_at_purchase (Float)  # Preço congelado (histórico)

Índices:
├─ orders.email (para buscar por rastreamento)
├─ orders.created_at (para filtrar por data)
└─ order_items.order_id (para listar itens de um pedido)
```

---

## 🔐 Segurança (MVP)

### Implementado ✅
- [ ] Validação com Pydantic (nenhum dado inválido entra)
- [ ] SQL Injection previsto (ORM SQLAlchemy)
- [ ] CORS configurado (restringir origens)
- [ ] Rate limiting básico (será melhorado em v0.2.0)

### Não está pronto para produção ⚠️
- ❌ Sem HTTPS (será adicionado no deploy)
- ❌ Sem autenticação (v0.2.0)
- ❌ Sem logging audit (v0.2.0)
- ❌ Sem proteção contra DDoS (será usado Railway/Render)

---

## ⚡ Performance & Otimizações

### Backend
- [ ] Lazy loading de produtos (paginação)
- [ ] Cache de produtos (TTL: 1 hora)
- [ ] Índices no BD (product_id, order.email)
- [ ] Serialização eficiente (Pydantic)

### Frontend
- [ ] Code splitting (lazy load views)
- [ ] Imagens otimizadas (WEBP)
- [ ] Cache HTTP (service worker - v0.2.0)
- [ ] Virtual scrolling (lista longa)

---

## 🧪 Testes

### Estratégia
```
Nível 1 (MVP v0.1.0): Unitários
├─ test_products.py: GET /produtos retorna lista
├─ test_orders.py: POST /pedidos cria order válida
└─ Models: validação de constraints

Nível 2 (v0.2.0): Integração
├─ Testes com MySQL real
├─ Fluxo completo (login → pedido)
└─ Migrations Alembic

Nível 3 (v0.3.0): E2E
├─ Playwright/Cypress: user flow completo
├─ Rastreamento em tempo real
└─ Notificações
```

---

## 🚀 Deployment (MVP)

### Local (Docker)
```bash
docker-compose up  # Backend + Frontend rodando
```

### Cloud (Railway/Render)
```
Frontend → Vercel/Railway
Backend → Railway/Render
Database → MySQL Cloud / Managed Service
```

---

## 📞 Perguntas Frequentes da Arquitetura

**P: Por que Pinia em vez de Vuex?**  
R: Pinia é mais simples, melhor TypeScript, composição melhor.

**P: Por que SQLAlchemy em vez de Tortoise ORM?**  
R: SQLAlchemy é padrão, mais estável, comunidade maior.

**P: Como lidamos com uploads de foto?**  
R: Não no MVP. v0.2.0: URL de imagem externa ou S3.

**P: Necessário Redis para cache?**  
R: Não no MVP. SQLite + in-memory é suficiente. v0.2.0 avalia.

---

**Última atualização:** 2026-09-01

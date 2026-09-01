# 🎯 Tarefas Disponíveis - v0.1.0 MVP

Abaixo estão as tarefas que podem ser peguem pela equipe. Organize-se por área!

---

## 🔧 Backend (FastAPI/Python)

### Prerequisito: Ter lido
- [ARQUITETURA.md](./ARQUITETURA.md)
- [SETUP_LOCAL.md](./SETUP_LOCAL.md)
- [API.md](./API.md)

---

### **Tier 1: Básico (Novo desenvolvedor? Comece aqui)**

| Tarefa | Descrição | Dificuldade | Tempo | Responsável | Status |
|--------|-----------|------------|-------|------------|--------|
| **T1.1** - Criar `requirements.txt` | Dependências FastAPI, SQLAlchemy, Pydantic, pytest | 🟢 Fácil | 15min | - | ⏳ |
| **T1.2** - Setup `config.py` | Leitura de .env, database config | 🟢 Fácil | 20min | - | ⏳ |
| **T1.3** - Criar `Product` Model | SQLAlchemy: id, name, price, description | 🟢 Fácil | 20min | - | ⏳ |
| **T1.4** - Criar `Order` Model | SQLAlchemy: id, email, items[], total, status | 🟡 Médio | 30min | - | ⏳ |

---

### **Tier 2: Intermediário**

| Tarefa | Descrição | Dificuldade | Tempo | Responsável | Status |
|--------|-----------|------------|-------|------------|--------|
| **T2.1** - Schemas Pydantic | ProductSchema, OrderSchema (validação) | 🟡 Médio | 30min | - | ⏳ |
| **T2.2** - Rota `GET /produtos` | Listar todos produtos com filtering | 🟡 Médio | 40min | - | ⏳ |
| **T2.3** - Rota `POST /pedidos` | Criar pedido anônimo (email + items) | 🟡 Médio | 50min | - | ⏳ |
| **T2.4** - Rota `GET /pedidos/{id}` | Buscar pedido por email + order_id | 🟡 Médio | 30min | - | ⏳ |
| **T2.5** - Middleware de Erro | Try-catch global, retornar JSON estruturado | 🟡 Médio | 40min | - | ⏳ |

---

### **Tier 3: Avançado (Resiliência)**

| Tarefa | Descrição | Dificuldade | Tempo | Responsável | Status |
|--------|-----------|------------|-------|------------|--------|
| **T3.1** - Idempotência | Hash+timestamp, cache no banco | 🔴 Hard | 60min | - | ⏳ |
| **T3.2** - Testes Unitários | pytest para models + routes | 🔴 Hard | 60min | - | ⏳ |
| **T3.3** - Documentação FastAPI | Decoradores @app.get, @app.post | 🔴 Hard | 30min | - | ⏳ |
| **T3.4** - Seed Database | Script para popular DB com produtos iniciais | 🔴 Hard | 45min | - | ⏳ |

---

## 🎨 Frontend (Vue.js/JavaScript)

### Prerequisito: Ter lido
- [ARQUITETURA.md](./ARQUITETURA.md)
- [SETUP_LOCAL.md](./SETUP_LOCAL.md)

---

### **Tier 1: Básico**

| Tarefa | Descrição | Dificuldade | Tempo | Responsável | Status |
|--------|-----------|------------|-------|------------|--------|
| **F1.1** - Setup `package.json` | Vue 3, Pinia, Axios, Vite | 🟢 Fácil | 10min | - | ⏳ |
| **F1.2** - Criar store Pinia | State: carrinho, produtos | 🟢 Fácil | 25min | - | ⏳ |
| **F1.3** - API client (axios) | Configurar base URL, interceptores | 🟡 Médio | 20min | - | ⏳ |
| **F1.4** - View `Products.vue` | Listar + adicionar ao carrinho | 🟡 Médio | 45min | - | ⏳ |

---

### **Tier 2: Intermediário**

| Tarefa | Descrição | Dificuldade | Tempo | Responsável | Status |
|--------|-----------|------------|-------|------------|--------|
| **F2.1** - View `Cart.vue` | Revisar carrinho, editar quantidade | 🟡 Médio | 40min | - | ⏳ |
| **F2.2** - View `OrderConfirmation.vue` | Formulário email, submit pedido | 🟡 Médio | 35min | - | ⏳ |
| **F2.3** - localStorage Persistência | Salvar carrinho entre sessões | 🟡 Médio | 25min | - | ⏳ |
| **F2.4** - Componente `ProductCard.vue` | Card reutilizável (nome, preço, botão) | 🟡 Médio | 30min | - | ⏳ |

---

### **Tier 3: Avançado (UX)**

| Tarefa | Descrição | Dificuldade | Tempo | Responsável | Status |
|--------|-----------|------------|-------|------------|--------|
| **F3.1** - Modal `ErrorModal.vue` | Mostrar erro de conexão, retry | 🔴 Hard | 40min | - | ⏳ |
| **F3.2** - Spinner `LoadingSpinner.vue` | Estados loading em requisições | 🔴 Hard | 20min | - | ⏳ |
| **F3.3** - Idempotência Frontend | Gerar Idempotency-Key no POST | 🔴 Hard | 25min | - | ⏳ |
| **F3.4** - Routing Vue Router | Navegar Products → Cart → Confirmation | 🔴 Hard | 35min | - | ⏳ |
| **F3.5** - Styling CSS/Tailwind | Layout responsivo, visual | 🔴 Hard | 60min | - | ⏳ |

---

## 📚 Documentação & DevOps

### **Tier 1: Essencial**

| Tarefa | Descrição | Dificuldade | Tempo | Responsável | Status |
|--------|-----------|------------|-------|------------|--------|
| **D1.1** - README.md raiz | Como rodar projeto completo | 🟢 Fácil | 20min | - | ⏳ |
| **D1.2** - SETUP_LOCAL.md | Step-by-step Backend + Frontend | 🟢 Fácil | 30min | - | ⏳ |
| **D1.3** - API.md | Documentação endpoints | 🟢 Fácil | 25min | - | ⏳ |
| **D1.4** - .env.example | Template variáveis Backend + Frontend | 🟢 Fácil | 10min | - | ⏳ |

---

### **Tier 2: DevOps**

| Tarefa | Descrição | Dificuldade | Tempo | Responsável | Status |
|--------|-----------|------------|-------|------------|--------|
| **D2.1** - Dockerfile Backend | Build image FastAPI | 🟡 Médio | 30min | - | ⏳ |
| **D2.2** - Dockerfile Frontend | Build image Vue.js | 🟡 Médio | 30min | - | ⏳ |
| **D2.3** - docker-compose.yml | Orquestrar Backend + Frontend | 🟡 Médio | 25min | - | ⏳ |
| **D2.4** - .gitignore | Python + Node patterns | 🟢 Fácil | 10min | - | ⏳ |

---

### **Tier 3: Planejamento**

| Tarefa | Descrição | Dificuldade | Tempo | Responsável | Status |
|--------|-----------|------------|-------|------------|--------|
| **D3.1** - ROADMAP.md | Visão futura (v0.2.0, v0.3.0) | 🟡 Médio | 40min | Tech Lead | ⏳ |
| **D3.2** - ARQUITETURA.md | Explicar design completo | 🟡 Médio | 60min | Tech Lead | ⏳ |
| **D3.3** - INCREMENTO_1_PLAN.md | Plano autenticação | 🟡 Médio | 45min | Tech Lead | ⏳ |
| **D3.4** - BD_SETUP.md | Guia para responsável MySQL | 🟡 Médio | 40min | Tech Lead | ⏳ |

---

## 🔄 Como Pegar Uma Tarefa

1. **Escolha sua área** (Backend, Frontend, Documentação)
2. **Selecione dificuldade** compatível com seu nível
3. **Abra uma branch:** `git checkout -b feature/T1.1-seu-nome`
4. **Implemente** seguindo padrões de código
5. **Faça PR** para `dev` com descrição clara
6. **Atualize este arquivo:** coloque seu nome + ✅ Pronto

---

## 📊 Status do MVP

```
Backend:
├─ Models: ⏳ (0/2)
├─ Schemas: ⏳ (0/1)
├─ Routes: ⏳ (0/4)
├─ Middleware: ⏳ (0/2)
└─ Testes: ⏳ (0/1)

Frontend:
├─ Store: ⏳ (0/1)
├─ Views: ⏳ (0/3)
├─ Components: ⏳ (0/2)
└─ Routing: ⏳ (0/1)

Docs:
├─ Core: ✅ (4/4)
├─ Setup: ⏳ (0/3)
└─ DevOps: ⏳ (0/4)
```

---

## 🎓 Rotação de Aprendizado

Sugestão de trilha para novos membros:

1. **Semana 1:** T1.1, T1.2, T1.3 (entender base)
2. **Semana 2:** T2.1, T2.2, F1.1 (conexão DB-Frontend)
3. **Semana 3:** T2.3, F1.4 (feature completa)
4. **Semana 4:** T3.1, F3.1 (resiliência)

---

## ❓ Dúvidas?

- **Sobre tarefa:** Comenta na issue/PR
- **Sobre arquitetura:** Lê [ARQUITETURA.md](./ARQUITETURA.md)
- **Geral:** Conversa com Tech Lead

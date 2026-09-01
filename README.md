# 🍕 Sistema de Delivery - MVP v0.1.0

**Aplicação de delivery com catálogo, carrinho e pedidos anônimos**

---

## 📖 Documentação Principal

> **Novo no projeto? Comece aqui:**
> 1. Leia [SETUP_LOCAL.md](./docs/SETUP_LOCAL.md) - Configure seu ambiente
> 2. Leia [ARQUITETURA.md](./docs/ARQUITETURA.md) - Entenda o design
> 3. Escolha tarefa em [TAREFAS_DISPONIVEIS.md](./docs/TAREFAS_DISPONIVEIS.md)
> 4. Leia [CONTRIBUINDO.md](./docs/CONTRIBUINDO.md) - Padrões de código

**Índice Completo:** [docs/README.md](./docs/README.md)

---

## 🚀 Quick Start (5 minutos)

### Backend

```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
python -c "from app.config import init_db; init_db()"
uvicorn main:app --reload
```

Backend em: `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend em: `http://localhost:5173`

---

## 📊 Escopo MVP

✅ **Funcionalidades Implementadas:**
- [ ] Catálogo de produtos (GET /produtos)
- [ ] Carrinho com localStorage
- [ ] Criar pedido anônimo (POST /pedidos)
- [ ] Rastreamento básico (GET /pedidos/{id})
- [ ] Resiliência de rede (retry, modals)
- [ ] Idempotência (sem pedidos duplicados)
- [ ] Tratamento global de erros
- [ ] Docker + docker-compose

❌ **Fora do MVP:**
- Autenticação (v0.2.0)
- Perfil de usuário (v0.2.0)
- Rastreamento real (v0.3.0)
- Notificações (v0.3.0)

---

## 🗺️ Roadmap

```
v0.1.0 (MVP)        → Catálogo + Carrinho + Pedido Anônimo
        ↓
v0.2.0 (Autenticação) → Login + Perfil + Favoritos + MySQL
        ↓
v0.3.0 (Rastreamento) → GPS + Notificações + Dashboard
        ↓
v0.4.0+ (Escala)      → Mobile + Entregadores + Analytics
```

Mais: [docs/ROADMAP.md](./docs/ROADMAP.md)

---

## 🏗️ Estrutura de Pastas

```
delivery-system/
├── backend/              # API Python (FastAPI)
│   ├── app/
│   │   ├── models/       # ORM SQLAlchemy
│   │   ├── schemas/      # Pydantic validation
│   │   ├── routes/       # Endpoints
│   │   └── middleware/   # Error handling, idempotência
│   ├── tests/            # pytest
│   ├── requirements.txt
│   └── main.py
│
├── frontend/             # Aplicação Vue.js
│   ├── src/
│   │   ├── views/        # Páginas (Products, Cart, Order)
│   │   ├── api/          # Axios client
│   │   ├── store/        # Pinia state
│   │   └── components/   # Reutilizáveis
│   └── package.json
│
├── docs/                 # Documentação completa
│   ├── README.md         # Índice
│   ├── ARQUITETURA.md    # Design técnico
│   ├── API.md            # Endpoints
│   ├── SETUP_LOCAL.md    # Como rodar
│   ├── CONTRIBUINDO.md   # Guia devs
│   ├── TAREFAS_DISPONIVEIS.md  # Work items
│   ├── DECISOES.md       # Decisões tomadas
│   ├── DISCUSSOES_ABERTAS.md   # O que decidir
│   ├── ROADMAP.md        # Versões futuras
│   ├── INCREMENTO_1_PLAN.md    # v0.2.0 plan
│   └── BD_SETUP.md       # MySQL guide
│
├── teste_1/              # MVP anterior (referência)
├── docker-compose.yml    # Orquestração
└── .gitignore
```

---

## 🛠️ Stack Tecnológico

| Aspecto | Tecnologia | Razão |
|---------|-----------|-------|
| Backend | FastAPI | Performance, documentação automática |
| Frontend | Vue.js 3 | Reatividade, simples, escalável |
| Database | SQLite (MVP) / MySQL (v0.2.0) | Prototipar rápido depois escalar |
| Validação | Pydantic | Declarativa, erros claros |
| Estado | Pinia | Simples, TypeScript-ready |
| HTTP | Axios | Retries, interceptores |
| Testes | pytest | Padrão Python, cobertura boa |

---

## 🔐 Segurança & Resiliência

### Implementado ✅
- Validação entrada (Pydantic)
- SQL Injection protection (ORM)
- CORS básico
- Middleware global de erro
- Idempotência (Hash + timestamp)
- localStorage persistência

### Não pronto ⚠️
- Sem HTTPS (será no deploy)
- Sem autenticação JWT (v0.2.0)
- Rate limiting básico (será Railway/Render)

---

## 📋 Decisões Arquiteturais

**Leia:** [docs/DECISOES.md](./docs/DECISOES.md)

Principais:
- ✅ MVP sem autenticação (pedidos anônimos)
- ✅ FastAPI + Vue.js stack
- ✅ Idempotência com Hash+timestamp
- ⚠️ Rastreamento simples no MVP (decidir em v0.2.0)
- ⚠️ User Model vazio (pronto para v0.2.0)

---

## ❓ Discussões Abertas

O que ainda precisa ser decidido em equipe:

1. **Idempotência:** Confirmar Hash+timestamp é a abordagem final
2. **Rastreamento v0.2.0:** Mecanismo (SMS, email, sistema web)
3. **Dados Pedido:** Campos adicionais (endereço, telefone, obs)
4. **Deploy:** Plataforma (Railway, Render, AWS)
5. **Testes Integração:** Quando e quem faz

**Leia:** [docs/DISCUSSOES_ABERTAS.md](./docs/DISCUSSOES_ABERTAS.md)

---

## 👥 Equipe & Responsabilidades

9 membros total. Veja: [teste_1/docs/equipe/responsabilidades.md](./teste_1/docs/equipe/responsabilidades.md)

**Tech Lead (você):**
- Arquitetura
- Code review
- Setup inicial

**Responsável BD:**
- MySQL setup (v0.2.0)
- Migrations (Alembic)
- Testes integração
- Guia: [docs/BD_SETUP.md](./docs/BD_SETUP.md)

**Outros Membros:**
- Peguem tarefas em [docs/TAREFAS_DISPONIVEIS.md](./docs/TAREFAS_DISPONIVEIS.md)
- Sigam [docs/CONTRIBUINDO.md](./docs/CONTRIBUINDO.md)

---

## 📝 Como Contribuir

1. Setup local: [docs/SETUP_LOCAL.md](./docs/SETUP_LOCAL.md)
2. Escolha tarefa: [docs/TAREFAS_DISPONIVEIS.md](./docs/TAREFAS_DISPONIVEIS.md)
3. Branch: `feature/T{numero}-seu-nome`
4. Código comentado, testes, PR para `dev`
5. Detalhes: [docs/CONTRIBUINDO.md](./docs/CONTRIBUINDO.md)

---

## 🐳 Docker

### Build & Run

```bash
docker-compose up
```

Acesso:
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

### Parar

```bash
docker-compose down
```

---

## 📞 Suporte & Comunicação

| Tipo | Onde |
|------|------|
| Dúvidas técnicas | GitHub Issues |
| Rápidas/Chat | Slack/Discord |
| Críticas | Video call |
| Documentação | Ver `/docs` |

---

## 📊 Status do Projeto

```
Backend Structure:      ⏳ (0% ready)
Frontend Structure:     ⏳ (0% ready)
Documentation:          ✅ (100% ready)
Tarefas Disponíveis:    ✅ (25 tarefas)
Roadmap:               ✅ (3 incrementos planejados)
```

---

## 🎯 Próximos Passos

1. ✅ Estrutura criada
2. ✅ Documentação completa
3. ⏳ **AGORA:** Equipe pega tarefas e começa desenvolvimento
4. ⏳ Testes e validação
5. ⏳ Code review e merge em `dev`
6. ⏳ Deploy local/Docker
7. ⏳ MVP pronto para validação

---

## 📜 Licença & Info

- **Projeto:** Sistema de Delivery (Acadêmico)
- **Equipe:** 9 membros
- **Metodologia:** Incremental + Scrum
- **Status:** MVP em desenvolvimento

---

## 🎉 Bem-vindo!

Esta é uma estrutura **production-ready** servindo como **modelo para a equipe**.

Código limpo, comentado, testado e documentado.

**Vamos construir algo incrível! 🚀**

---

**Última atualização:** 2026-09-01  
**Próxima revisão:** 2026-09-15 (MVP pronto)

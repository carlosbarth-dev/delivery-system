<<<<<<< HEAD
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
=======
# Sistema de Delivery

Projeto acadêmico desenvolvido com práticas de uma equipe de software: escopo definido, documentação técnica, fluxo de contribuição e revisão de código.

## Objetivo

Construir um MVP de marketplace de delivery. O cliente deve conseguir descobrir um restaurante, consultar o cardápio, montar um pedido e acompanhá-lo, sem criar uma conta.

O escopo oficial está em [docs/ROADMAP.md](./docs/ROADMAP.md). Antes de implementar qualquer funcionalidade, confirme que ela pertence ao MVP.

## Comece aqui

1. Leia o [índice da documentação](./docs/README.md).
2. Configure o ambiente com o [guia de setup](./docs/SETUP_LOCAL.md).
3. Entenda os componentes e limites técnicos em [ARQUITETURA.md](./docs/ARQUITETURA.md).
4. Receba uma tarefa do Team Lead e siga o [guia de contribuição](./docs/CONTRIBUINDO.md).

## Stack planejada

| Camada | Tecnologia |
| --- | --- |
| Frontend | Vue 3, Vite, Pinia e Axios |
| Backend | Python, FastAPI, SQLAlchemy e Pydantic |
| Banco de dados do MVP | MySQL |
| Ambiente local | Docker Compose (opcional) |

## Status

O repositório contém a estrutura inicial do projeto. O MVP está em desenvolvimento; a situação das entregas é acompanhada pelo Team Lead, não por documentos públicos de tarefas.

## Executar localmente

Consulte [SETUP_LOCAL.md](./docs/SETUP_LOCAL.md). Os comandos básicos são:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

Em outro terminal:

```powershell
>>>>>>> origin/dev
cd frontend
npm install
npm run dev
```

<<<<<<< HEAD
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
=======
## Estrutura

```text
backend/    API FastAPI
frontend/   Aplicação Vue
docs/       Documentação do projeto
PR-models/  Modelos de pull request e apoio à colaboração
```
>>>>>>> origin/dev

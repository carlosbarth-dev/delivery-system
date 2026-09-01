# 📋 Decisões Arquiteturais - v0.1.0

## Decisões Confirmadas ✅

### **1. Stack Tecnológico**
- **Backend:** FastAPI + SQLAlchemy (Python)
- **Frontend:** Vue.js 3 + Pinia + Axios + Vite
- **Database:** SQLite (MVP) → MySQL (após v0.2.0)
- **Versionamento:** Git/GitHub (branches main/dev)
- **Deploy:** Docker + Railway/Render (a discutir depois)

**Raciocínio:**
- FastAPI: Performance, documentação automática, validação Pydantic integrada
- Vue.js: Reatividade, curva aprendizado suave para equipe
- SQLite MVP: Prototipagem rápida, sem infraestrutura complexa

---

### **2. Autenticação no MVP**
- **Status:** ❌ NÃO incluída no MVP v0.1.0
- **Quando:** Incremento 1 (v0.2.0)
- **Tipo:** JWT (tokens stateless)
- **Estrutura:** Criada vazia no código, pronta para ativar

**Raciocínio:**
- MVP deve ser o mais simples possível (pedidos anônimos)
- Facilita onboarding para novos membros da equipe
- Estrutura já preparada reduz retrabalho no Incremento 1

---

### **3. User Model**
- **Status:** Estrutura vazia no código (pronta para v0.2.0)
- **Campos MVP:** Nenhum em uso
- **Campos v0.2.0:** id, email, senha_hash, favoritos[], pedidos[], created_at

**Raciocínio:**
- Não queremos quebrar código ao adicionar autenticação
- Estrutura base organiza pensamento futuro

---

### **4. Dados do Pedido Anônimo**
- **Campo de identificação:** Email (para rastreamento simples)
- **Campos no pedido:**
  ```
  {
    id: int (UUID único)
    email: string (para rastreamento)
    items: [{product_id, quantity, price}]
    total_price: float
    status: string (pending, preparing, ready, completed)
    created_at: datetime
    updated_at: datetime
  }
  ```
- **Decision maker:** Tech Lead + discussão em equipe se mudar

**Raciocínio:**
- Email é suficiente para MVP (rastreamento básico)
- Status simples permite evolução para real (v0.3.0)

---

### **5. Idempotência (Anti-Duplicação de Pedidos)**
- **Abordagem:** Hash do carrinho + timestamp (gerado automaticamente no Frontend)
- **Header HTTP:** `Idempotency-Key`
- **Status:** ⚠️ REVISAR com equipe se trocar de abordagem

**Raciocínio:**
- Previne pedidos duplicados em caso de retry de rede
- Hash garante mesmo carrinho = mesma key
- Timestamp previne colisão

**TODO:** Documentar decisão final em `docs/DISCUSSOES_ABERTAS.md`

---

### **6. Rastreamento de Pedidos**
- **MVP v0.1.0:** Simples (email + order_id)
- **Incremento 1:** Básico (status updates)
- **Incremento 2+:** Real (integração com delivery)

**Raciocínio:**
- MVP não precisa de complexidade de rastreamento real
- Prepare estrutura para depois (status field existe)

**TODO:** Decidir mecanismo no Incremento 1

---

### **7. Resiliência & Network**
- **Frontend:**
  - Estados de loading em todas as requisições
  - Carrinho salvo em localStorage (persiste offline)
  - Modal de erro/reconexão em caso de falha
  - Retry automático com backoff exponencial

- **Backend:**
  - Middleware global de tratamento de exceções
  - Validação de entrada com Pydantic
  - Logs estruturados (pronto para v0.2.0)

**Raciocínio:**
- Entregas são críticas (não podem perder pedido)
- Rede pode falhar a qualquer momento

---

### **8. Estrutura de Código Como Referência**
- **Objetivo:** Código serve de modelo para os 8 membros
- **Estratégia:**
  - Comentários em TODAS as linhas (exceto óbvias)
  - Comments referenciam documentação ("Ver ARQUITETURA.md linha X")
  - Exemplos claros em cada módulo
  - Testes como documentação

**Raciocínio:**
- Equipe vai crescer: precisa de clareza
- Código não é escrever, é comunicar

---

## Decisões Pendentes ⚠️

Ver `DISCUSSOES_ABERTAS.md`

---

## Histórico de Decisões

| Data | Decisão | Responsável | Status |
|------|---------|-------------|--------|
| 2026-09-01 | Stack: FastAPI + Vue.js | Tech Lead | ✅ Confirmada |
| 2026-09-01 | MVP sem autenticação | Tech Lead | ✅ Confirmada |
| 2026-09-01 | SQLite → MySQL (v0.2.0) | Tech Lead | ✅ Confirmada |
| 2026-09-01 | Idempotência com Hash+timestamp | Tech Lead | ⚠️ Revisar com equipe |

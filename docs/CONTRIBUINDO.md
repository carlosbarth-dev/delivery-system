# 🤝 Guia de Contribuição - Como Trabalhar no Projeto

Bem-vindo! Este é um guia para os 8 membros da equipe.

---

## 📖 Antes de Começar

1. Leia [SETUP_LOCAL.md](./SETUP_LOCAL.md) - configure ambiente
2. Leia [ARQUITETURA.md](./ARQUITETURA.md) - entenda design
3. Escolha tarefa em [TAREFAS_DISPONIVEIS.md](./TAREFAS_DISPONIVEIS.md)
4. Abra uma branch e comece! 🚀

---

## 🎯 Workflow: De Tarefa a Merge

### 1️⃣ Escolha Tarefa

```
Ver TAREFAS_DISPONIVEIS.md
Encontre tarefa com ⏳ (não iniciada)
Exemplo: T1.1 - Criar requirements.txt
```

### 2️⃣ Crie Branch

```bash
git checkout dev  # Sempre partir de dev
git pull origin dev

git checkout -b feature/T1.1-seu-nome

# Exemplos:
# feature/T2.3-alice-rotas-pedidos
# feature/T3.1-bob-idempotencia
# feature/F1.4-carol-vue-produtos
```

**Convenção de nome:**
```
feature/T{numero}-{seu-nome}-{descrição}
```

### 3️⃣ Desenvolva

```bash
# Faça suas mudanças
# Commit frequentemente
git add .
git commit -m "feat: T1.1 - criar requirements.txt com FastAPI"
```

**Padrão de commit:**
```
feat:     Nova feature
fix:      Bug fix
docs:     Documentação
refactor: Refatoração
test:     Testes
chore:    Setup, dependências
```

### 4️⃣ Escreva Testes

```bash
# Se backend, escreva teste
cd backend
pytest tests/test_seus_testes.py

# Se frontend, escreva testes (v0.2.0)
```

### 5️⃣ Faça PR (Pull Request)

```bash
git push origin feature/seu-nome
# Abra PR no GitHub
```

**Template de PR:**

```markdown
## Descrição
O que você fez? Por quê?

## Tarefa
Closes #42 (ou referência a TAREFAS_DISPONIVEIS.md)

## Testes
- [ ] Testes criados/atualizados
- [ ] Testes passam localmente

## Checklist
- [ ] Código comentado (quando necessário)
- [ ] Sem erros de linting
- [ ] Documentação atualizada
- [ ] Sem conflitos com dev
```

### 6️⃣ Code Review

- Tech Lead ou peer review
- Ajuste se houver comentários
- Aprovação = Merge!

### 7️⃣ Merge & Deploy

```bash
# Automático (GitHub Actions - v0.2.0+)
# Ou manual:
git checkout dev
git merge feature/seu-nome
git push origin dev
```

---

## 💻 Padrões de Código

### Python (Backend)

**Formatação:**
```bash
# Use Black
pip install black
black backend/
```

**Linting:**
```bash
# Use Flake8
pip install flake8
flake8 backend/
```

**Tipo:**
```python
# Sempre com type hints
from typing import List, Optional

def get_products(
    skip: int = 0,
    limit: int = 20
) -> List[dict]:
    """Retorna lista de produtos.
    
    Args:
        skip: Quantos pular (paginação)
        limit: Quantos retornar
        
    Returns:
        Lista de dicts com produto info
    """
    return db.query(Product).offset(skip).limit(limit).all()
```

**Comentários:**
```python
# ✅ BOM: Explica PORQUÊ
def calculate_total(items: List[OrderItem]) -> float:
    # Multiplicar quantidade * preço e somar
    # (preço congelado no pedido para histórico)
    return sum(item.quantity * item.price_at_purchase for item in items)

# ❌ RUIM: Óbvio demais
def get_user(user_id: int):
    # Obter usuário por ID
    return db.query(User).filter(User.id == user_id).first()
```

**Erros:**
```python
# ✅ BOM: Trata exceção específica
try:
    order = db.query(Order).filter(Order.id == order_id).first()
except SQLAlchemyError as e:
    logger.error(f"DB error: {e}")
    raise HTTPException(status_code=500, detail="Database error")

# ❌ RUIM: Catch genérico
try:
    order = db.query(Order).filter(Order.id == order_id).first()
except:
    pass
```

### JavaScript/Vue (Frontend)

**Formatação:**
```bash
# Use Prettier
npm install --save-dev prettier
npx prettier --write src/
```

**Linting:**
```bash
# Use ESLint
npm install --save-dev eslint eslint-plugin-vue
npx eslint src/
```

**Componentes Vue:**
```vue
<template>
  <div class="products-container">
    <!-- Estrutura clara, sem lógica complexa -->
    <ProductCard 
      v-for="product in products" 
      :key="product.id"
      :product="product"
      @add-to-cart="addToCart"
    />
  </div>
</template>

<script setup>
// Usar setup syntax (Vue 3)
import { ref, computed, onMounted } from 'vue'
import ProductCard from '@/components/ProductCard.vue'

const products = ref([])
const loading = ref(false)

// Comentar lógica complexa
const totalPrice = computed(() => {
  // Somar preços ajustados (percentual de desconto não vem aqui)
  return products.value.reduce((sum, p) => sum + p.price, 0)
})

onMounted(async () => {
  await fetchProducts()
})

async function fetchProducts() {
  loading.value = true
  try {
    products.value = await api.getProducts()
  } catch (error) {
    console.error('Erro ao buscar:', error)
  } finally {
    loading.value = false
  }
}

function addToCart(product) {
  store.addToCart(product)
}
</script>

<style scoped>
.products-container {
  display: grid;
  gap: 1rem;
}
</style>
```

---

## 🧪 Testes

### Backend (pytest)

```python
# tests/test_products.py
import pytest
from app.models import Product
from app.routes import products

def test_get_products_empty():
    """Teste quando nenhum produto existe"""
    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json() == {"total": 0, "items": []}

def test_get_products_with_filter():
    """Teste filtro por nome"""
    # Setup: criar produto
    db.add(Product(name="Pizza", price=10.0))
    db.commit()
    
    # Test
    response = client.get("/produtos?search=pizza")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1
    assert response.json()["items"][0]["name"] == "Pizza"

def test_create_order_success():
    """Teste criação de pedido bem-sucedida"""
    response = client.post("/pedidos", json={
        "email": "test@example.com",
        "items": [{"product_id": 1, "quantity": 2, "price": 10.0}],
        "total_price": 20.0
    })
    assert response.status_code == 201
    assert response.json()["order_id"] > 0
```

**Rodar testes:**
```bash
cd backend
pytest -v  # Verbose
pytest --cov=app  # Com cobertura
```

### Frontend

Será adicionado em v0.2.0 com Vitest/Cypress.

---

## 📝 Documentação

**Quando você termina uma tarefa:**

1. ✅ Atualize [TAREFAS_DISPONIVEIS.md](./TAREFAS_DISPONIVEIS.md)
   ```markdown
   | **T1.1** - Criar `requirements.txt` | ... | ✅ Alice | 2026-09-05
   ```

2. ✅ Se alterou design, atualize [ARQUITETURA.md](./ARQUITETURA.md)

3. ✅ Se descobriu algo novo, adicione em [DECISOES.md](./DECISOES.md)

4. ✅ Se ainda há dúvida, anote em [DISCUSSOES_ABERTAS.md](./DISCUSSOES_ABERTAS.md)

---

## 🚫 O QUE NÃO FAZER

❌ Commitar `venv/`, `node_modules/`, `.env` (sigiloso)  
❌ Pushear direto para `main` (sempre via PR em `dev`)  
❌ Mudar decisões já tomadas sem avisar  
❌ Código sem testes  
❌ Merges para `dev` sem aprovação  

---

## 🆘 Precisa de Ajuda?

### Erro de setup?
→ Ver [SETUP_LOCAL.md](./SETUP_LOCAL.md)

### Entender arquitetura?
→ Ver [ARQUITETURA.md](./ARQUITETURA.md)

### Especificação de API?
→ Ver [API.md](./API.md)

### Qual tarefa pegar?
→ Ver [TAREFAS_DISPONIVEIS.md](./TAREFAS_DISPONIVEIS.md)

### Dúvida técnica?
→ Abra issue ou converse com Tech Lead

---

## 🎓 Rotação de Aprendizado (Sugestão)

**Semana 1: Fundações**
- Setup local + primeiros commits
- Tasks: T1.1, T1.2 (setup)
- Objetivo: Entender como o projeto funciona

**Semana 2: Backend**
- Implementar Models + Routes
- Tasks: T1.3, T1.4, T2.1, T2.2
- Objetivo: API funcional

**Semana 3: Frontend**
- Componentes + Estado (Pinia)
- Tasks: F1.1, F1.4, F2.1
- Objetivo: Frontend fácil conversando com API

**Semana 4: Resiliência**
- Middleware, Testes, Error handling
- Tasks: T3.1, T3.2, F3.1
- Objetivo: Produção-ready

---

## 📊 Métricas de Qualidade

Para cada merge em `dev`:
- ✅ 100% testes passando
- ✅ Cobertura > 80%
- ✅ Código comentado (onde necessário)
- ✅ Sem warnings de linting
- ✅ Documentação atualizada

---

## 🚀 Performance & Boas Práticas

### Backend
- [ ] Valide entrada com Pydantic
- [ ] Use ORM (SQLAlchemy) não SQL direto
- [ ] Log estruturado (será melhorado v0.2.0)
- [ ] Trate exceções globalmente
- [ ] Evite query N+1 (carregamento lazy)

### Frontend
- [ ] Reutilize componentes
- [ ] Use Pinia para estado compartilhado
- [ ] localStorage para dados offline-first
- [ ] Loading states em requisições
- [ ] Trate erros com modais/notificações

---

## 🔄 Manutenção de Branches

```bash
# Manter branch atualizada
git fetch origin
git rebase origin/dev

# Se houver conflitos
# 1. Resolve manualmente
# 2. git add .
# 3. git rebase --continue
# 4. git push -f origin feature/seu-nome
```

---

## 📞 Comunicação

**Reuniões:**
- Daily standup: 10min (status)
- Planning: Antes de novo incremento
- Retrospectiva: Após cada versão

**Chat:**
- Dúvidas técnicas: GitHub Issues
- Rápidas: Slack/Discord
- Críticas: Video call com Tech Lead

---

**Última atualização:** 2026-09-01  
**Bem-vindo à equipe! 🎉**

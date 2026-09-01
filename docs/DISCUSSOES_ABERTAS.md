# 🔴 Discussões Abertas - Decidir em Equipe

## ⚠️ Itens que PRECISAM de Discussão

### **1. Idempotência - Mecanismo de Prevenção de Pedidos Duplicados**

**Status Atual:** Hash do carrinho + timestamp (automático)

**Opções:**

```
A) Hash do carrinho + timestamp (ATUAL)
   ✅ PROS: Automático, sem interferência do usuário
   ❌ CONTRAS: Se usuário editar carrinho, perde histórico
   Função: idempotency_key = hash(items + timestamp)

B) UUID aleatório gerado no Frontend
   ✅ PROS: Simples, não quebra se carrinho mudar
   ❌ CONTRAS: Manual, pode gerar duplicação se usuário não esperar
   Função: idempotency_key = uuid.uuid4()

C) Order ID do Backend
   ✅ PROS: Garantido único
   ❌ CONTRAS: Requer 2 requisições (POST com UUID temp, depois GET real)
```

**Decisão:** Implementamos (A), mas **REVISAR em equipe** antes de v0.1.0 final

**Arquivo:** `backend/app/middleware/idempotency.py` (linha ~45)

**Próximo Passo:** Abrir discussão no GitHub/reunião

---

### **2. Rastreamento de Pedidos - Mecanismo Final**

**Status Atual:** Email + order_id (MVP)

**Roadmap:**
- **v0.1.0:** Email único para buscar pedido
- **v0.2.0:** Decidir mecanismo de rastreamento real
- **v0.3.0+:** Integrar com API de delivery real

**Opções para v0.2.0:**

```
A) SMS com código (baixa complexidade)
B) Email updates (médium)
C) Sistema web completo (alta)
D) QR code + webhook (muito alta)
```

**Arquivo de TODO:** `backend/app/routes/orders.py` (linha ~30)

**Próximo Passo:** Decidir após v0.1.0 funcionar

---

### **3. Dados do Pedido - Campos Adicionais**

**Campos Atuais (Confirmados):**
```python
{
  id, email, items[], total_price, status, 
  created_at, updated_at
}
```

**Campos Pendentes (Questões):**

- [ ] Endereço de entrega? (Será em v0.2.0 com usuário)
- [ ] Telefone? (Alternativa ao email para rastreamento)
- [ ] Observações? (ex: "Sem cebola", "Entrega rápida")
- [ ] Foto de comprovante? (Será em v0.2.0)
- [ ] Cupom/Código promocional? (Será depois)

**Decision Maker:** Toda a equipe (não só Tech Lead)

**Próximo Passo:** Reunião para definir modelo final

---

### **4. Deploy - Plataforma & Automação**

**Status Atual:** A discutir

**Opções:**

| Opção | Custo | Facilidade | Escalabilidade |
|-------|-------|-----------|-----------------|
| Heroku | 💰 Medium | 🟢 Fácil | 🟡 Média |
| Railway | 💰 Low | 🟢 Fácil | 🟢 Alta |
| Render | 💰 Low | 🟢 Fácil | 🟢 Alta |
| AWS (EC2) | 💰 Low | 🟡 Médio | 🟢 Alta |
| DigitalOcean | 💰 Low | 🟡 Médio | 🟢 Alta |

**Recomendação Tech Lead:** Railway ou Render (simples + grátis até limite)

**Próximo Passo:** Decidir em reunião

---

### **5. Banco de Dados - Timing da Migração para MySQL**

**Status Atual:**
- MVP (v0.1.0): SQLite
- v0.2.0: Migrar para MySQL

**Questões:**

- [ ] Instalar MySQL antes de v0.1.0? (Prepara para testes)
- [ ] Usar Docker Compose com MySQL agora?
- [ ] Responsável pelo BD começa antes ou depois de v0.1.0 pronto?

**Decision Maker:** Tech Lead + Responsável BD

**Próximo Passo:** Agendar com responsável do BD

---

### **6. Teste de Integração - Timing**

**Status Atual:** A fazer após MySQL ser conectado

**Questões:**

- [ ] Fazer testes unitários antes (v0.1.0)?
- [ ] Testes de integração só depois que BD estiver real?
- [ ] Quem escreve: Tech Lead ou Responsável BD?

**Arquivo de Placeholder:** `backend/tests/test_integration_db.py`

**Próximo Passo:** Decidir em reunião de planejamento

---

## 📝 Template para Decisão

Quando a equipe decidir um tópico acima:

1. **Editar este arquivo** com resultado
2. **Mover para `DECISOES.md`** seção de "Decisões Confirmadas"
3. **Atualizar código** com comentários finais
4. **Criar issue** se necessário implementação

---

## 🔔 Checklist de Reunião

- [ ] Decidir Idempotência (opção final)
- [ ] Decidir Rastreamento v0.2.0
- [ ] Confirmar Dados Pedido (com equipe)
- [ ] Escolher plataforma Deploy
- [ ] Agendar BD com responsável
- [ ] Definir timing de testes integração

**Data Sugerida:** Próxima reunião da equipe

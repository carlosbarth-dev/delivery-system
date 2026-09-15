<<<<<<< HEAD
# 🗺️ Roadmap - Sistema de Delivery

Visão completa do projeto: de onde viemos, onde estamos, e para onde vamos.

---

## 🚀 Versões Planejadas

```
MVP (v0.1.0)
    │
    ├─ Catálogo de produtos
    ├─ Carrinho (localStorage)
    ├─ Pedido anônimo
    ├─ Rastreamento básico (email)
    └─ Deploy em Docker
            │
            v
   Incremento 1 (v0.2.0)
    │
    ├─ Autenticação JWT
    ├─ Perfil de usuário
    ├─ Histórico de pedidos
    ├─ Favoritos
    ├─ MySQL real (saindo de SQLite)
    └─ Testes de integração
            │
            v
   Incremento 2 (v0.3.0)
    │
    ├─ Rastreamento real (GPS + status)
    ├─ Notificações (email/SMS)
    ├─ Sistema de avaliação
    ├─ Cupons/Promoções
    └─ Analytics & Dashboard
            │
            v
   Incremento 3+ (v0.4.0+)
    │
    ├─ App Mobile (React Native)
    ├─ Sistema de delivery (entregadores)
    ├─ Pagamento online
    ├─ Integração com APIs reais
    └─ Clustering/Escalabilidade
```

---

## 📋 MVP (v0.1.0) - O QUE TEMOS AGORA

**Status:** 🚧 Em desenvolvimento

### Features Implementadas ✅
- [ ] Catálogo de produtos com filtro
- [ ] Adicionar/remover do carrinho
- [ ] localStorage persistência
- [ ] Formulário de pedido anônimo
- [ ] Endpoint de rastreamento básico
- [ ] Tratamento de erros global
- [ ] Idempotência de pedidos
- [ ] Dockerização

### Arquitetura
- **Backend:** FastAPI + SQLAlchemy + SQLite
- **Frontend:** Vue.js + Pinia + Axios
- **Database:** SQLite em arquivo
- **Deploy:** Docker (local/Railway)

### Testes
- [ ] Unitários (Backend)
- [ ] Integração (simulado com SQLite)

### Documentação
- [x] README
- [x] Decisões arquiteturais
- [x] Roadmap (este arquivo)
- [x] Tarefas disponíveis
- [ ] Guia de contribuição
- [ ] API specification

### Timeline Estimada
- **Início:** 2026-09-01
- **MVP Pronto:** 2026-09-15 (2 semanas)
- **Deployment Local:** 2026-09-15

---

## 🔐 Incremento 1 (v0.2.0) - Autenticação & Perfil

**Status:** 📋 Planejamento

### Features
- [ ] Login/Registro com JWT
- [ ] Perfil de usuário (dados pessoais)
- [ ] Histórico de pedidos (linked ao usuário)
- [ ] Favoritos (salvar produtos)
- [ ] Carrinho salvo no servidor (não localStorage)
- [ ] Perfil de endereço (para entregas)

### Infraestrutura
- [ ] MySQL instalado + Alembic migrations
- [ ] Testes de integração com BD real
- [ ] Refresh tokens (segurança JWT)
- [ ] Password hashing (bcrypt)

### Timeline Estimada
- **Início:** 2026-09-15 (após MVP)
- **Pronto:** 2026-10-01 (2-3 semanas)
- **Razão para delay:** Maturar MVP, ajustar feedback

### Decisões Pendentes ⚠️
- [ ] Campos adicionais do usuário?
- [ ] Integração com email confirmação?
- [ ] Social login (Google/GitHub)?

---

## 🚚 Incremento 2 (v0.3.0) - Rastreamento Real

**Status:** 💡 Ideação

### Features
- [ ] Rastreamento real-time (GPS)
- [ ] Status updates (preparando → a caminho → entregue)
- [ ] Notificações por email/SMS
- [ ] Sistema de avaliação (cliente avalia entrega)
- [ ] Cupons/Códigos promocionais
- [ ] Dashboard administrativo (v0.3.1)

### Infraestrutura
- [ ] WebSocket para live updates
- [ ] Integração com serviço de delivery real
- [ ] Fila de jobs (Celery/Bull)
- [ ] Cache Redis (rastreamento)

### Timeline Estimada
- **Início:** 2026-10-01
- **Pronto:** 2026-11-01 (4 semanas)
- **Razão:** Depende de parceria com delivery

---

## 📱 Incremento 3+ (v0.4.0+) - Escalabilidade

**Status:** 🎯 Visão futura

### Possíveis Features
- [ ] App Mobile (React Native / Flutter)
- [ ] Portal do entregador (app dedicada)
- [ ] Integração com múltiplas plataformas de delivery
- [ ] Sistema de assinatura/premium
- [ ] Analytics & BI Dashboard
- [ ] Microserviços (se necessário escalabilidade)

### Timing
- Após v0.3.0 maduro em produção

---

## 📊 Comparação: MVP vs v0.2.0 vs v0.3.0

| Aspecto | MVP (v0.1.0) | v0.2.0 | v0.3.0 |
|---------|--------------|--------|--------|
| **Usuário Anônimo** | ✅ | ❌ (Com conta) | ❌ |
| **Carrinho** | localStorage | BD (usuário) | BD |
| **Histórico Pedidos** | ❌ | ✅ | ✅ |
| **Favoritos** | ❌ | ✅ | ✅ |
| **Rastreamento** | Email simples | Email updates | Real-time GPS |
| **Notificações** | ❌ | Email | Email + SMS |
| **Autenticação** | ❌ | JWT | JWT + OAuth |
| **Database** | SQLite | MySQL | MySQL + Redis |
| **Deploy** | Docker local | Cloud | Cloud HA |
| **Testes** | Unitários | Integração | E2E |
| **Team Size** | 1-2 dev | 3-4 dev | 5+ dev |

---

## 🎯 Objetivos Por Fase

### v0.1.0 - MVP
> "**Funciona!** Podemos fazer e receber um pedido sem login"
- Demonstrar conceito funciona
- Validar com usuários reais
- Estabelecer arquitetura padrão

### v0.2.0 - Autenticação
> "**Persistência!** Meus pedidos, favoritos, dados salvos"
- Retenção de usuários
- Múltiplas compras
- Personalização

### v0.3.0 - Rastreamento
> "**Confiabilidade!** Acompanho meu pedido em tempo real"
- Transparência
- Satisfação do cliente
- Reduz suporte

### v0.4.0+ - Escala
> "**Crescimento!** Suporta 10x usuários, múltiplas cidades"
- Mobile
- Entregadores
- Analytics
- B2B

---

## 🔧 Tech Debt & Melhorias Contínuas

### v0.1.0 → v0.2.0
- [ ] Refatorar models (preparar para usuário)
- [ ] Adicionar logging estruturado
- [ ] Melhorar testes
- [ ] Documentar API com OpenAPI/Swagger

### v0.2.0 → v0.3.0
- [ ] Otimizar queries BD
- [ ] Implementar cache estratégico
- [ ] Melhorar performance Frontend (code splitting)
- [ ] Monitoramento em produção

### v0.3.0 → v0.4.0
- [ ] Refatorar monolito em microserviços (se necessário)
- [ ] Containerização completa
- [ ] CI/CD robusto
- [ ] Disaster recovery

---

## 📅 Timeline Estimada Completa

```
2026-09-01 ─┬─ MVP Pronto       (v0.1.0)
            │
2026-09-15 ─┤
            │
2026-10-01 ─┼─ Auth + Perfil     (v0.2.0)
            │
2026-10-15 ─┤
            │
2026-11-01 ─┼─ Rastreamento Real (v0.3.0)
            │
2026-11-15 ─┤
            │
2026-12-01 ─┼─ Análise v0.4.0
            │
2027-01-01 ─┴─ Roadmap Revisado
```

---

## 👥 Crescimento da Equipe

```
MVP (v0.1.0):        1-2 devs (Tech Lead + 1)
v0.2.0:              3-4 devs
v0.3.0:              5-6 devs
v0.4.0+:             8+ devs (frontend, backend, mobile, devops)
```

---

## 🚨 Riscos & Mitigações

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Escalabilidade BD | 🔴 Alto | Planar MySQL migrations cedo |
| Rede instável | 🔴 Alto | Resiliência no cliente (localStorage) |
| Mudança de escopo | 🟡 Médio | Keep MVP pequeno, iterar rápido |
| Falta de testes | 🟡 Médio | Testes desde v0.1.0 |
| Débito técnico | 🟡 Médio | Code review rigoroso |
| Comunicação equipe | 🟡 Médio | Docs + reuniões regulares |

---

## 📞 Próximos Passos

### Agora (v0.1.0)
1. ✅ Finalizar estrutura Backend + Frontend
2. ⏳ Implementar features MVP
3. ⏳ Testes e debug
4. ⏳ Deploy Docker local
5. ⏳ Code review com equipe

### Depois (v0.2.0 planning)
1. Retrospectiva v0.1.0
2. Definir requisitos autenticação
3. Planejar migrations BD
4. Atribuir tarefas novo incremento

---

**Última atualização:** 2026-09-01  
**Próxima revisão:** 2026-09-15
=======
# Roadmap e escopo do produto

## MVP — Marketplace de delivery

O MVP demonstra o fluxo completo de compra em um restaurante. Ele não pretende reproduzir todos os recursos de plataformas comerciais.

### Funcionalidades incluídas

| Área | Requisito |
| --- | --- |
| Descoberta | Listar restaurantes com status aberto/fechado, distância e tempo estimado. |
| Cardápio | Exibir categorias, produtos, foto/URL de imagem, descrição, preço e observação quando permitida. |
| Carrinho | Adicionar, remover e alterar quantidades; recalcular subtotal e total. |
| Entrega | Escolher entrega ou retirada; calcular a taxa de entrega. |
| Checkout | Finalizar sem login com os dados mínimos necessários para o pedido. |
| Pagamento | Permitir Pix e dinheiro na entrega. |
| Pedido | Criar pedido, exibir status e tempo estimado de entrega. |
| Resiliência | Preservar carrinho/pedido localmente, apresentar erros claros e evitar pedido duplicado. |

### Requisitos funcionais do MVP

| ID | Requisito |
| --- | --- |
| RF-01 | O sistema deve listar restaurantes com nome, status aberto/fechado, distância e tempo estimado. |
| RF-02 | O cliente deve consultar o cardápio de um restaurante por categoria. |
| RF-03 | Cada produto deve informar nome, descrição, preço, imagem/URL, disponibilidade e se aceita observação. |
| RF-04 | O cliente deve adicionar produtos ao carrinho, remover itens e alterar quantidades. |
| RF-05 | O carrinho deve aceitar itens de apenas um restaurante por pedido. |
| RF-06 | O cliente deve escolher entrega ou retirada; endereço é obrigatório somente para entrega. |
| RF-07 | O sistema deve calcular subtotal, taxa de entrega e total no backend. |
| RF-08 | O checkout anônimo deve aceitar somente Pix ou dinheiro na entrega no MVP. |
| RF-09 | O sistema deve criar um pedido com identificador, itens, valores, modalidade, pagamento e estado inicial. |
| RF-10 | O cliente deve consultar o pedido e visualizar seu status e tempo estimado. |
| RF-11 | O sistema deve impedir a duplicação de pedido quando a mesma solicitação for repetida. |
| RF-12 | O carrinho e a referência do pedido devem sobreviver ao recarregamento da página. |

### Fluxo do usuário

```text
Abrir aplicação
    ↓
Consultar restaurantes disponíveis
    ↓
Abrir cardápio e escolher produtos
    ↓
Montar carrinho de um único restaurante
    ↓
Escolher entrega ou retirada
    ↓
Informar dados obrigatórios e escolher Pix ou dinheiro
    ↓
Revisar valores calculados pelo sistema e confirmar pedido
    ↓
Receber identificação do pedido e acompanhar o status
```

### Requisitos não funcionais essenciais

- O backend valida dados, disponibilidade e valores antes de persistir o pedido.
- Erros devem ser claros para o cliente e não expor detalhes internos.
- A criação de pedido deve usar uma chave de idempotência.
- Dados locais do carrinho e pedido devem ser tratados de forma segura e recuperável em falha de rede.
- O MVP deve ser demonstrável em ambiente local com dados de exemplo.

### Regras de escopo

- Um pedido pertence a um único restaurante.
- O servidor calcula preços, taxa e total; o frontend nunca é fonte de verdade financeira.
- O checkout anônimo deve coletar endereço somente para entrega e contato mínimo para acompanhamento.
- Idempotência é obrigatória na criação de pedido: repetir a mesma solicitação não pode gerar dois pedidos.
- “Canal de emergência” e “alerta de atraso” podem ser apresentados como informações de contato e regra de interface no MVP; não exigem integração externa de mensagens.

### Fora do MVP

- Conta, login, perfil, histórico e favoritos.
- Pagamento on-line integrado ou confirmação automática de Pix.
- Rastreamento GPS, WebSocket, notificações por e-mail/SMS e aplicativo de entregador.
- Painel administrativo, cupons, avaliações e analytics.
- Infraestrutura de produção, microsserviços ou migração para banco gerenciado.

## Próximos incrementos

| Incremento | Direção |
| --- | --- |
| 1 | Autenticação, perfil, endereços salvos, histórico e favoritos. |
| 2 | Notificações e rastreamento mais completo. |
| Futuro | Painel do restaurante, entregadores, pagamentos integrados e escala. |

## Critério de conclusão do MVP

Uma pessoa consegue escolher um restaurante, montar um pedido válido, escolher entrega ou retirada, finalizar sem login e consultar o status do pedido. O fluxo possui validações, tratamento de erro e testes dos cenários essenciais.

**Fonte de verdade do escopo.** Qualquer funcionalidade nova deve ser aprovada antes de entrar no desenvolvimento.
>>>>>>> origin/dev

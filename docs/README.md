# 📚 Documentação - Sistema de Delivery v0.1.0

Bem-vindo! Este diretório contém toda a documentação técnica, decisões e planejamento do projeto.

## 🗂️ Índice de Documentação

### **Fundações do Projeto**
- [ROADMAP.md](./ROADMAP.md) - Visão geral, versões, incrementos e timeline
- [DECISOES.md](./DECISOES.md) - Decisões arquiteturais e tecnológicas
- [DISCUSSOES_ABERTAS.md](./DISCUSSOES_ABERTAS.md) - O que ainda precisa ser decidido em equipe

### **Desenvolvimento**
- [ARQUITETURA.md](./ARQUITETURA.md) - Design da API, estrutura de pastas, fluxo de dados
- [API.md](./API.md) - Especificação dos endpoints (MVP)
- [SETUP_LOCAL.md](./SETUP_LOCAL.md) - Como rodar o projeto localmente
- [CONTRIBUINDO.md](./CONTRIBUINDO.md) - Guia para novos desenvolvedores (os 8 membros)

### **Próximos Passos**
- [INCREMENTO_1_PLAN.md](./INCREMENTO_1_PLAN.md) - Planejamento autenticação + perfil
- [BD_SETUP.md](./BD_SETUP.md) - Instruções para responsável de BD (MySQL)

### **Organização do Projeto**
- [../teste_1/docs/equipe/responsabilidades.md](../teste_1/docs/equipe/responsabilidades.md) - Papéis e responsabilidades da equipe
- [TAREFAS_DISPONIVEIS.md](./TAREFAS_DISPONIVEIS.md) - Trabalhos para pegar (por área)

---

## 🚀 Quick Start

```bash
# Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py

# Frontend
cd frontend
npm install
npm run dev
```

Mais detalhes em [SETUP_LOCAL.md](./SETUP_LOCAL.md)

---

## 📈 Versões & Timeline

**MVP (v0.1.0):** Catálogo + Carrinho + Pedido Anônimo  
**Incremento 1 (v0.2.0):** Autenticação + Perfil + Favoritos  
**Incremento 2 (v0.3.0):** Rastreamento Real + Notificações  

Ver [ROADMAP.md](./ROADMAP.md) para detalhes completos.

---

## 🤝 Como Contribuir

1. Leia [CONTRIBUINDO.md](./CONTRIBUINDO.md)
2. Escolha uma tarefa em [TAREFAS_DISPONIVEIS.md](./TAREFAS_DISPONIVEIS.md)
3. Abra uma branch `feature/seu-nome` a partir de `dev`
4. Siga o padrão de código (comentários, testes, etc)

---

## 📞 Dúvidas?

- Técnicas: Abra uma issue
- Arquitetura: Ver [ARQUITETURA.md](./ARQUITETURA.md)
- Próximas features: Ver [INCREMENTO_1_PLAN.md](./INCREMENTO_1_PLAN.md)

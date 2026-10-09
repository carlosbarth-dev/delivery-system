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

O projeto tem o fluxo inicial de checkout e pagamentos organizado no backend. Catálogo, checkout anônimo e integração completa com o frontend seguem em desenvolvimento, conforme o [roadmap](./docs/ROADMAP.md).

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
cd frontend
npm install
npm run dev
```

## Estrutura

```text
backend/    API FastAPI
frontend/   Aplicação Vue
docs/       Documentação do projeto
PR-models/  Modelos de pull request e apoio à colaboração
```

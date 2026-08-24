# Neon Delivery

Sistema de delivery em Flask com visual cyberpunk, login, painel administrativo, cadastro de produtos com foto e carrinho de compras.

## Como executar

1. Crie um ambiente virtual: `python -m venv .venv`
2. Ative-o no PowerShell: `.\.venv\Scripts\Activate.ps1`
3. Instale as dependências: `pip install -r requirements.txt`
4. Copie `.env.example` para `.env` e preencha `DATABASE_URL` com seu PostgreSQL.
5. Inicie: `python app.py`
6. Acesse `http://127.0.0.1:5000`

Na primeira inicialização são criados o banco/tabelas e o usuário administrador:

- E-mail: `admin@neondelivery.com`
- Senha: `admin123`

Altere a senha antes de colocar o projeto em produção. Sem `DATABASE_URL`, o projeto usa SQLite local (`delivery.db`) somente para facilitar testes.

## Organização

- `app.py`: rotas, autenticação, pedidos e produtos.
- `templates/`: páginas HTML.
- `static/css/`: identidade visual.
- `static/js/`: interações do carrinho e painel.
- `static/uploads/`: fotos enviadas dos produtos (criada automaticamente).

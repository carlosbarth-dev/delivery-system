# Setup local

## Pré-requisitos

- Python 3.9 ou superior
- Node.js 18 ou superior e npm
- Git
- Docker Desktop (opcional)

## Backend

No PowerShell, a partir da raiz do repositório:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

A API deve iniciar em `http://localhost:8000`. Quando disponível, consulte `http://localhost:8000/docs`.

## Frontend

Em outro terminal:

```powershell
cd frontend
npm install
npm run dev
```

O Vite informa no terminal a URL local, normalmente `http://localhost:5173`.

## Configuração local

O projeto fornece modelos de configuração. Crie os arquivos locais antes de iniciar os serviços e nunca faça commit deles:

```powershell
Copy-Item backend\.env.example backend\.env
Copy-Item frontend\.env.example frontend\.env
```

O backend usa SQLite por padrão. Para o MVP, mantenha `DATABASE_URL=sqlite:///./delivery.db` e `VITE_API_URL=http://localhost:8000` no frontend, salvo orientação diferente do Team Lead.

## Docker

Com Docker Desktop em execução, na raiz do projeto:

```powershell
docker compose up --build
```

Para encerrar, use `docker compose down`.

## Verificações

Antes de abrir um PR, execute os comandos de validação disponíveis no componente alterado:

```powershell
cd backend
pytest
```

```powershell
cd frontend
npm run build
```

Se algum comando ainda não estiver configurado no repositório, registre isso no PR; não declare uma validação como executada sem tê-la realizado.

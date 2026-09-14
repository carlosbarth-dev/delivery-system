# Catálogo e segurança — parte do Pedro

Este módulo é a minha contribuição isolada para o delivery. Ele roda sem o
front-end e sem os arquivos da `main`: usa SQLite local para demonstrar o
catálogo e define o formato que o site poderá consumir quando juntarmos as
partes. Não há pedido nem cobrança nesta versão.

## O que eu fiz

- Criei uma API de leitura com `GET /produtos` e `GET /healthcheck`.
- Modelei `categoria` e `produto`, com preço decimal, disponibilidade e relação
  entre as tabelas.
- Tirei credenciais do código: a configuração real fica em `backend/.env`,
  enquanto o Git recebe apenas `.env.example`.
- Limitei o CORS a origens informadas e a lista a 100 produtos. Erros de banco
  não revelam SQL nem credenciais ao cliente.
- Escrevi testes de funcionamento e segurança e preparei uma migração para
  adaptar o catálogo ao MySQL do grupo.

Isso não substitui o front, a API ou o banco de ninguém. Ainda não fiz login,
painel administrativo, endereço, pedido nem pagamento. Essas funções exigirão
regras e testes próprios antes de publicar o sistema.

## Rodando só esta parte

Na raiz da branch, com Python 3.11 ou mais recente:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r backend\pedro_integration\requirements-dev.txt
.venv\Scripts\python.exe -m uvicorn pedro_integration.api:app --app-dir backend --host 127.0.0.1 --port 8000
```

Abra `http://127.0.0.1:8000/healthcheck`, `http://127.0.0.1:8000/produtos`
e `http://127.0.0.1:8000/docs`. Não é preciso instalar o front.
No desenvolvimento, a API cria `backend/pedro_integration/pedro_delivery.db`
e põe três produtos de exemplo somente se a tabela estiver vazia. O banco
local é ignorado pelo Git.

Se precisar mudar a configuração, use
`backend/pedro_integration/.env.example` como referência e crie
`backend/.env`. Nunca publique esse arquivo com senhas. Em
`APP_ENV=production`, a API exige `DATABASE_URL` e `CORS_ORIGINS`, não
cria tabelas e não insere exemplos.

O contrato para o front é `GET /produtos`: a resposta traz uma lista
`items`; cada produto tem `id`, `name`, `price` e `description`. O preço
vem como texto decimal. Quando houver integração, o front pode definir
`VITE_API_URL` com o endereço público da API. Não coloque senhas em
`VITE_*`: elas aparecem no navegador. A senha do banco fica só na API.

## Ligando ao MySQL do grupo depois

Esta branch não contém `models/database/delivery.sql` do Victor. A migração
`migrations/001_catalogo_mysql.sql` pressupõe que as tabelas `categoria` e
`produto` desse esquema já existam. Antes de aplicá-la, a pessoa do banco
deve testar em uma cópia, fazer backup se houver dados e conferir preços
negativos. Ela acrescenta `descricao` e impede preço abaixo de zero; não
apaga produtos.

Para esta API de leitura, use um usuário próprio com apenas `SELECT` em
`categoria` e `produto`. Não use `root`. Configure a `DATABASE_URL` no
`backend/.env` com o driver `mysql+mysqlconnector://`. A API falha ao iniciar
se a tabela ou a coluna necessária não existir.

Ainda não testei em MySQL real porque não havia servidor MySQL nem Docker
neste ambiente. O teste opcional usa `TEST_MYSQL_URL` com conta de leitura e
é pulado quando essa variável não está definida. Não considero essa parte
pronta para produção antes do teste com o banco do grupo.

## O que a segurança cobre — e o que falta

As consultas são parametrizadas pelo SQLAlchemy; `GET /produtos` aceita
limite entre 1 e 100. O healthcheck consulta o banco de verdade. O CORS
aceita apenas origens explícitas de `CORS_ORIGINS`. Erros de banco recebem
mensagem genérica. Para a web, `SEED_DEMO=false`, HTTPS e banco fora da
internet são necessários.

CORS não é autenticação. Aqui, só catálogo e saúde são rotas públicas.
Quando o grupo criar cadastro ou pedidos, precisará definir login,
permissões, validação de endereço e idempotência contra pedidos duplicados.

## Testando e apresentando

Na raiz da branch:

```powershell
cd backend
..\.venv\Scripts\python.exe -m pytest pedro_integration\tests -q
```

Os testes usam SQLite temporário, sem tocar no banco de outra pessoa.
Cobrem produtos, disponibilidade, limite inválido, tentativa de injeção
no parâmetro, CORS, integridade dos dados, erro seguro e ausência de rotas
de pagamento. Em 14/09/2026, 9 passaram e 1 teste MySQL foi pulado.

Para explicar à professora: mostro o `.env.example` e por que o `.env` real
fica fora do Git; rodo a API e consulto `/healthcheck` e `/produtos`;
mostro os modelos e a migração; executo os testes; e termino dizendo o
que ainda depende da integração com o grupo.

Referências: [OWASP — segurança de banco](https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html),
[FastAPI — CORS](https://fastapi.tiangolo.com/tutorial/cors/) e
[Vite — variáveis de ambiente](https://vite.dev/guide/env-and-mode).

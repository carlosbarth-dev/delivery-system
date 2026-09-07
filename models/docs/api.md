# API Delivery

O arquivo `database/api/main.py` define as rotas da API. Para ela aparecer no
navegador, o servidor precisa estar em execução.

No terminal, entre na pasta do arquivo:

```powershell
cd models/database/api
python main.py
```

Ou use o comando direto do Uvicorn (recomendado durante o desenvolvimento):

```powershell
cd models/database/api
python -m uvicorn main:app --reload --port 8001
```

Com o terminal aberto e a mensagem `Uvicorn running on ...`, acesse:

- `http://127.0.0.1:8001/` — rota inicial;
- `http://127.0.0.1:8001/health` — confirmação de que a API está online;
- `http://127.0.0.1:8001/docs` — página interativa gerada automaticamente pelo FastAPI.

`127.0.0.1` (ou `localhost`) significa **apenas este computador**. Para outras
pessoas acessarem pela internet, é necessário publicar a aplicação em um serviço
de hospedagem ou configurar um túnel; iniciar o Uvicorn local não cria um site
público.

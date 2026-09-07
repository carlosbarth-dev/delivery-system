from fastapi import FastAPI

app = FastAPI(title="API Delivery")


@app.get("/")
def inicio():
    return {
        "mensagem": "API Delivery funcionando!"
    }


@app.get("/health")
def health_check():
    """Rota simples para verificar se o servidor está online."""
    return {"status": "online"}


if __name__ == "__main__":
    # Permite iniciar com: python main.py
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)

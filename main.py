"""
PONTO DE ENTRADA DA APLICAÇÃO (main.py)
----------------------------------------
Este é o arquivo principal, executado pelo servidor Uvicorn.

Aqui nós:
  1. Criamos a aplicação FastAPI.
  2. Mantemos os endpoints originais da ATIVIDADE 01
     (o "Hello World" e o endpoint que retorna o nome completo).
  3. Conectamos (include_router) a CAMADA DE APRESENTAÇÃO de Pessoas,
     que por baixo usa as camadas de Negócio, Dados e Modelo.

Como executar:
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload

Documentação interativa (gerada automaticamente pelo FastAPI):
    http://localhost:8000/docs
"""

from fastapi import FastAPI

from app.routers.pessoa_router import router as pessoa_router

app = FastAPI(
    title="biancaAPI",
    description="Sistema em Python com FastAPI usando arquitetura em camadas.",
    version="2.0.0",
)

# Conecta a camada de apresentação (rotas de pessoas) à aplicação.
app.include_router(pessoa_router)


# ---------------------------------------------------------------------------
# ENDPOINTS DA ATIVIDADE 01 (mantidos para reaproveitar a API anterior)
# ---------------------------------------------------------------------------
@app.get("/", tags=["Atividade 01"])
def read_root():
    """Endpoint inicial padrão (Hello World)."""
    return {"Hello": "World"}


@app.get("/nome", tags=["Atividade 01"])
def retornar_nome():
    """Endpoint que retorna o nome completo (Atividade 01)."""
    return {"nome_completo": "Bianca Silva"}

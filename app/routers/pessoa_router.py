"""
CAMADA DE APRESENTAÇÃO (Presentation / Router Layer)
-----------------------------------------------------
Responsável por EXPOR a API para o mundo externo (HTTP).

Aqui definimos as rotas (endpoints) e os métodos HTTP (GET, POST, PUT, DELETE).
Esta camada:
  - Recebe a requisição HTTP e os dados (já validados pela camada de modelo).
  - Chama a camada de negócio (service) para executar a operação.
  - Traduz as exceções de negócio em respostas HTTP (status code + mensagem).

Ela NÃO contém regra de negócio nem acesso a dados — apenas orquestra a
comunicação entre o cliente HTTP e a camada de serviço.
"""

from typing import List

from fastapi import APIRouter, HTTPException, status

from app.models.pessoa import Pessoa, PessoaCreate, PessoaUpdate
from app.services.pessoa_service import (
    PessoaNaoEncontradaError,
    RegraNegocioError,
    pessoa_service,
)

# Agrupa todas as rotas de "pessoas" sob o prefixo /pessoas.
router = APIRouter(prefix="/pessoas", tags=["Pessoas"])


@router.get("/", response_model=List[Pessoa], summary="Listar todas as pessoas")
def listar_pessoas():
    return pessoa_service.listar_pessoas()


@router.get("/{pessoa_id}", response_model=Pessoa, summary="Buscar pessoa por id")
def buscar_pessoa(pessoa_id: int):
    try:
        return pessoa_service.buscar_pessoa(pessoa_id)
    except PessoaNaoEncontradaError as erro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(erro))


@router.post(
    "/",
    response_model=Pessoa,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar nova pessoa",
)
def criar_pessoa(dados: PessoaCreate):
    try:
        return pessoa_service.criar_pessoa(dados)
    except RegraNegocioError as erro:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro))


@router.put("/{pessoa_id}", response_model=Pessoa, summary="Atualizar pessoa")
def atualizar_pessoa(pessoa_id: int, dados: PessoaUpdate):
    try:
        return pessoa_service.atualizar_pessoa(pessoa_id, dados)
    except PessoaNaoEncontradaError as erro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(erro))
    except RegraNegocioError as erro:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro))


@router.delete(
    "/{pessoa_id}",
    status_code=status.HTTP_200_OK,
    summary="Remover pessoa",
)
def remover_pessoa(pessoa_id: int):
    try:
        pessoa_service.remover_pessoa(pessoa_id)
        return {"mensagem": f"Pessoa com id {pessoa_id} removida com sucesso."}
    except PessoaNaoEncontradaError as erro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(erro))

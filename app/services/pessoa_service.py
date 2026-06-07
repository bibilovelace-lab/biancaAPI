"""
CAMADA DE NEGÓCIO (Service Layer)
----------------------------------
Responsável pelas REGRAS DE NEGÓCIO da aplicação.

É a "ponte" entre a camada de apresentação (rotas) e a camada de dados
(repositório). Aqui ficam as decisões e validações da aplicação, por exemplo:
  - Não permitir cadastrar duas pessoas com o mesmo e-mail.
  - Avisar quando uma pessoa não for encontrada.

Esta camada NÃO sabe falar HTTP (não retorna status code diretamente):
ela apenas aplica as regras e LANÇA exceções quando algo está errado.
A camada de apresentação é quem traduz essas exceções em respostas HTTP.
"""

from typing import List

from app.models.pessoa import Pessoa, PessoaCreate, PessoaUpdate
from app.repositories.pessoa_repository import pessoa_repository


class RegraNegocioError(Exception):
    """Erro de regra de negócio (ex.: e-mail duplicado)."""
    pass


class PessoaNaoEncontradaError(Exception):
    """Erro lançado quando a pessoa não existe."""
    pass


class PessoaService:
    def __init__(self) -> None:
        # A camada de negócio usa a camada de dados (repositório).
        self.repository = pessoa_repository

    def listar_pessoas(self) -> List[Pessoa]:
        return self.repository.listar()

    def buscar_pessoa(self, pessoa_id: int) -> Pessoa:
        pessoa = self.repository.buscar_por_id(pessoa_id)
        if pessoa is None:
            raise PessoaNaoEncontradaError(
                f"Pessoa com id {pessoa_id} não encontrada."
            )
        return pessoa

    def criar_pessoa(self, dados: PessoaCreate) -> Pessoa:
        # REGRA DE NEGÓCIO: não permitir e-mail duplicado.
        if self.repository.buscar_por_email(dados.email) is not None:
            raise RegraNegocioError(
                f"Já existe uma pessoa cadastrada com o e-mail {dados.email}."
            )
        return self.repository.criar(dados)

    def atualizar_pessoa(self, pessoa_id: int, dados: PessoaUpdate) -> Pessoa:
        # Garante que a pessoa existe antes de atualizar.
        self.buscar_pessoa(pessoa_id)

        # REGRA DE NEGÓCIO: o novo e-mail não pode pertencer a OUTRA pessoa.
        existente = self.repository.buscar_por_email(dados.email)
        if existente is not None and existente.id != pessoa_id:
            raise RegraNegocioError(
                f"O e-mail {dados.email} já está em uso por outra pessoa."
            )

        return self.repository.atualizar(pessoa_id, dados)

    def remover_pessoa(self, pessoa_id: int) -> None:
        if not self.repository.remover(pessoa_id):
            raise PessoaNaoEncontradaError(
                f"Pessoa com id {pessoa_id} não encontrada."
            )


# Instância única do serviço, usada pela camada de apresentação.
pessoa_service = PessoaService()

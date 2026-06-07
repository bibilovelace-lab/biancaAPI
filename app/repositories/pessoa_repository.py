"""
CAMADA DE DADOS (Repository Layer)
-----------------------------------
Responsável por GUARDAR e RECUPERAR os dados.

Nesta atividade a persistência é EM MEMÓRIA: usamos uma simples lista Python
(_banco) que funciona como se fosse a nossa "tabela" de pessoas.
(Obs.: por ser em memória, os dados são reiniciados toda vez que o servidor
reinicia — em um projeto real, aqui entraria um banco de dados como o SQLite.)

Esta camada NÃO conhece regras de negócio e NÃO conhece HTTP.
Ela só sabe fazer as operações básicas de CRUD sobre a lista:
Create, Read, Update e Delete.
"""

from typing import List, Optional

from app.models.pessoa import Pessoa, PessoaCreate, PessoaUpdate


class PessoaRepository:
    def __init__(self) -> None:
        # "Banco de dados" em memória: uma lista de objetos Pessoa.
        self._banco: List[Pessoa] = []
        # Controla o próximo id a ser gerado (auto incremento).
        self._proximo_id: int = 1

    def listar(self) -> List[Pessoa]:
        """Retorna todas as pessoas cadastradas."""
        return self._banco

    def buscar_por_id(self, pessoa_id: int) -> Optional[Pessoa]:
        """Retorna a pessoa com o id informado, ou None se não existir."""
        for pessoa in self._banco:
            if pessoa.id == pessoa_id:
                return pessoa
        return None

    def buscar_por_email(self, email: str) -> Optional[Pessoa]:
        """Retorna a pessoa com o e-mail informado, ou None se não existir."""
        for pessoa in self._banco:
            if pessoa.email == email:
                return pessoa
        return None

    def criar(self, dados: PessoaCreate) -> Pessoa:
        """Cria uma nova pessoa, gerando um id automático."""
        nova_pessoa = Pessoa(id=self._proximo_id, **dados.model_dump())
        self._banco.append(nova_pessoa)
        self._proximo_id += 1
        return nova_pessoa

    def atualizar(self, pessoa_id: int, dados: PessoaUpdate) -> Optional[Pessoa]:
        """Atualiza os dados de uma pessoa existente."""
        for indice, pessoa in enumerate(self._banco):
            if pessoa.id == pessoa_id:
                atualizada = Pessoa(id=pessoa_id, **dados.model_dump())
                self._banco[indice] = atualizada
                return atualizada
        return None

    def remover(self, pessoa_id: int) -> bool:
        """Remove a pessoa pelo id. Retorna True se removeu, False se não achou."""
        for indice, pessoa in enumerate(self._banco):
            if pessoa.id == pessoa_id:
                del self._banco[indice]
                return True
        return False


# Instância única (singleton simples) compartilhada pela aplicação,
# para que a mesma lista em memória seja usada durante toda a execução.
pessoa_repository = PessoaRepository()

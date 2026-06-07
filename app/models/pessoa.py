"""
CAMADA DE MODELO (Model Layer)
--------------------------------
Responsável por DEFINIR a estrutura dos dados que entram e saem da API.

Usamos o Pydantic (que vem junto com o FastAPI) para:
  - Validar automaticamente os dados recebidos (ex.: e-mail no formato certo).
  - Gerar a documentação automática no /docs.
  - Garantir que cada camada troque dados em um formato bem definido.

Aqui não existe regra de negócio nem acesso a dados: é apenas o "contrato"
de como uma Pessoa é representada no sistema.
"""

from pydantic import BaseModel, EmailStr, Field


class PessoaBase(BaseModel):
    """Campos comuns usados na criação e na atualização de uma pessoa."""

    nome_completo: str = Field(
        ...,
        min_length=3,
        max_length=120,
        description="Nome completo da pessoa",
        examples=["Bianca Silva"],
    )
    email: EmailStr = Field(
        ...,
        description="E-mail válido da pessoa",
        examples=["praazerbianca@hotmail.com"],
    )
    idade: int = Field(
        ...,
        ge=0,
        le=120,
        description="Idade da pessoa (0 a 120)",
        examples=[25],
    )


class PessoaCreate(PessoaBase):
    """Modelo usado quando o cliente ENVIA dados para criar uma pessoa."""
    pass


class PessoaUpdate(PessoaBase):
    """Modelo usado quando o cliente ENVIA dados para atualizar uma pessoa."""
    pass


class Pessoa(PessoaBase):
    """
    Modelo COMPLETO devolvido pela API.
    Inclui o 'id' gerado pelo sistema, além dos campos da base.
    """

    id: int = Field(..., description="Identificador único gerado pelo sistema")

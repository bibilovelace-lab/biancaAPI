# biancaAPI — Sistema em Python com FastAPI (Arquitetura em Camadas)

Atividade 02 — sistema em Python utilizando **arquitetura em camadas**,
reaproveitando a API FastAPI criada na Atividade 01.

O sistema gerencia **Pessoas** (CRUD completo) em memória, separando
claramente as responsabilidades em 4 camadas.

**Autora:** Bianca Silva

Após iniciar o servidor, a documentação interativa fica disponível em
<http://localhost:8000/docs>.

## Arquitetura em Camadas

```
Cliente HTTP (navegador / Insomnia / Postman)
        │
        ▼
┌─────────────────────────────────────────────┐
│  CAMADA DE APRESENTAÇÃO  (app/routers)        │  ← rotas HTTP, status codes
├─────────────────────────────────────────────┤
│  CAMADA DE NEGÓCIO       (app/services)       │  ← regras (ex.: e-mail único)
├─────────────────────────────────────────────┤
│  CAMADA DE DADOS         (app/repositories)   │  ← lista em memória (CRUD)
├─────────────────────────────────────────────┤
│  CAMADA DE MODELO        (app/models)         │  ← schemas / validação Pydantic
└─────────────────────────────────────────────┘
```

| Camada            | Arquivo                                  | Responsabilidade                              |
|-------------------|------------------------------------------|-----------------------------------------------|
| Apresentação      | `app/routers/pessoa_router.py`           | Expor endpoints HTTP e traduzir erros         |
| Negócio (Service) | `app/services/pessoa_service.py`         | Regras de negócio e validações                |
| Dados (Repository)| `app/repositories/pessoa_repository.py`  | Guardar/recuperar dados (lista em memória)    |
| Modelo (Model)    | `app/models/pessoa.py`                   | Estrutura e validação dos dados (Pydantic)    |
| Entrada           | `main.py`                                | Inicia o app e conecta as rotas               |

## Como executar

```bash
# 1. (opcional) criar e ativar ambiente virtual
python -m venv myenv
myenv\Scripts\activate        # Windows
# source myenv/bin/activate   # Linux/Mac

# 2. instalar dependências
pip install -r requirements.txt

# 3. rodar o servidor
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Acesse a documentação interativa em: <http://localhost:8000/docs>

## Endpoints

### Atividade 01 (mantidos)
- `GET /` → `{"Hello": "World"}`
- `GET /nome` → retorna o nome completo

### Atividade 02 — Pessoas (CRUD em camadas)
- `GET    /pessoas`          → lista todas as pessoas
- `GET    /pessoas/{id}`     → busca uma pessoa por id
- `POST   /pessoas`          → cadastra uma nova pessoa
- `PUT    /pessoas/{id}`     → atualiza uma pessoa
- `DELETE /pessoas/{id}`     → remove uma pessoa

### Exemplo de corpo (POST/PUT)
```json
{
  "nome_completo": "Bianca Silva",
  "email": "praazerbianca@hotmail.com",
  "idade": 25
}
```

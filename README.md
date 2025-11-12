# League Manager API

API RESTful para gerenciamento de equipes, membros, inventário e finanças. Construída com FastAPI, SQLAlchemy e PostgreSQL.

## Descrição

O League Manager é um sistema de gerenciamento que permite:

- Autenticação e autorização baseada em roles (Administrador, Líder, Membro)
- Gerenciamento de equipes e seus membros
- Controle de inventário por equipe
- Gerenciamento de transações financeiras
- Sistema de permissões hierárquico

## Requisitos

- Python 3.13 ou superior
- PostgreSQL
- Poetry (gerenciador de dependências)

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/nicolassm145/manager-api.git
cd manager-api
```

2. Instale as dependências com Poetry:

```bash
poetry install
```

3. Configure as variáveis de ambiente:

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
SECRET_KEY=sua_chave_secreta_aqui
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

4. Execute as migrações (o SQLAlchemy criará as tabelas automaticamente):

```bash
poetry run python run.py
```

## Como Executar

### Desenvolvimento

Execute o servidor de desenvolvimento com hot-reload:

```bash
poetry run python run.py
```

Ou diretamente com uvicorn:

```bash
poetry run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

A API estará disponível em: `http://127.0.0.1:8000`

### Documentação Interativa

Após iniciar o servidor, acesse:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Estrutura do Projeto

```
manager-api/
├── app/
│   ├── api/
│   │   ├── deps.py              # Dependências e middlewares
│   │   └── v1/
│   │       ├── auth.py          # Endpoints de autenticação
│   │       ├── users.py         # Endpoints de usuários
│   │       └── equipes.py       # Endpoints de equipes
│   ├── core/
│   │   ├── config.py            # Configurações da aplicação
│   │   └── database.py          # Configuração do banco de dados
│   ├── models/
│   │   ├── base.py              # Modelo base
│   │   ├── user.py              # Modelo de usuário
│   │   ├── equipe.py            # Modelo de equipe
│   │   ├── item.py              # Modelo de item
│   │   └── transacao.py         # Modelo de transação
│   ├── schemas/
│   │   ├── user.py              # Schemas Pydantic de usuário
│   │   ├── equipe.py            # Schemas Pydantic de equipe
│   │   ├── item.py              # Schemas Pydantic de item
│   │   └── transacao.py         # Schemas Pydantic de transação
│   ├── services/
│   │   ├── user_service.py      # Lógica de negócio de usuários
│   │   └── equipe_service.py    # Lógica de negócio de equipes
│   ├── utils/
│   │   └── security.py          # Funções de segurança (hash, JWT)
│   └── main.py                  # Aplicação FastAPI principal
├── .env                         # Variáveis de ambiente
├── pyproject.toml               # Configuração do Poetry
├── run.py                       # Script para iniciar o servidor
├── ENDPOINTS.md                 # Documentação detalhada dos endpoints
└── README.md                    # Este arquivo
```

## Principais Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **PostgreSQL** - Banco de dados relacional
- **Pydantic** - Validação de dados e serialização
- **Python-JOSE** - Criação e validação de tokens JWT
- **Passlib & Bcrypt** - Hash de senhas
- **Uvicorn** - Servidor ASGI de alta performance

## Sistema de Permissões

### Roles Disponíveis

1. **Administrador**

   - Acesso completo ao sistema
   - Pode gerenciar todas as equipes e usuários
   - Pode criar, editar e deletar qualquer recurso

2. **Líder**

   - Gerencia sua própria equipe
   - Pode criar e editar membros da sua equipe
   - Pode visualizar e editar dados da sua equipe

3. **Membro**
   - Acesso limitado aos próprios dados
   - Pode visualizar informações da sua equipe
   - Pode editar apenas seu email e senha

## Principais Endpoints

### Autenticação

- `POST /api/v1/auth/login` - Fazer login

### Usuários

- `POST /api/v1/users/criar` - Criar usuário
- `GET /api/v1/users/listarTudo` - Listar todos os usuários
- `GET /api/v1/users/listar/{user_id}` - Obter usuário por ID
- `PUT /api/v1/users/atualizar/{user_id}` - Atualizar usuário
- `DELETE /api/v1/users/deletar/{user_id}` - Desativar usuário

### Equipes

- `POST /api/v1/equipes/criar` - Criar equipe
- `GET /api/v1/equipes/listAll` - Listar todas as equipes
- `GET /api/v1/equipes/listar/{equipe_id}` - Obter equipe por ID
- `PUT /api/v1/equipes/atualizar/{equipe_id}` - Atualizar equipe
- `DELETE /api/v1/equipes/deletar/{equipe_id}` - Deletar equipe
- `GET /api/v1/equipes/{equipe_id}/membros` - Listar membros da equipe

## Licença

Este projeto está sob a licença especificada no arquivo [LICENSE](LICENSE).

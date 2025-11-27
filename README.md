# League Manager API

![Python](https://img.shields.io/badge/Python-3.13%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0%2B-009688)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%2B-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-336791)
![License](https://img.shields.io/badge/License-MIT-green)

API RESTful robusta para gerenciamento de equipes, membros, inventário e finanças. Desenvolvida com foco em performance e escalabilidade utilizando FastAPI, SQLAlchemy e PostgreSQL.

## 📋 Descrição

O **League Manager** é uma solução completa para administração de guildas, clãs ou grupos de jogos, oferecendo:

- **Segurança**: Autenticação JWT e controle de acesso baseado em roles (RBAC).
- **Organização**: Gestão hierárquica de equipes e membros.
- **Recursos**: Controle de inventário e itens por equipe.
- **Finanças**: Registro e histórico de transações financeiras.

## ✨ Funcionalidades

- **Autenticação & Autorização**:
    - Login seguro com JWT.
    - Níveis de acesso: Administrador, Líder e Membro.
- **Gestão de Equipes**:
    - Criação e edição de equipes.
    - Atribuição de líderes e membros.
- **Inventário**:
    - Adição e remoção de itens.
    - Visualização de inventário por equipe.
- **Financeiro**:
    - Registro de entradas e saídas.
    - Histórico de transações.
- **Integração Google**:
    - **Calendar**: Criação automática de calendários de equipe e agendamento de eventos.
    - **Drive**: Organização de arquivos e documentos por equipe.

## 🛠️ Requisitos

- **Python** 3.13 ou superior
- **PostgreSQL** (Banco de dados)
- **Poetry** (Gerenciador de dependências)

## 🚀 Instalação

1. **Clone o repositório**

```bash
git clone https://github.com/nicolassm145/manager-api.git
cd manager-api
```

2. **Instale as dependências**

```bash
poetry install
```

3. **Configure o ambiente**

Copie o arquivo de exemplo e configure suas variáveis:

```bash
cp .env_example .env
```

Edite o arquivo `.env` com suas configurações do PostgreSQL, chaves de segurança e credenciais do Google:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
SECRET_KEY=sua_chave_secreta_super_segura
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Google Integration
GOOGLE_CLIENT_ID=seu_client_id
GOOGLE_CLIENT_SECRET=seu_client_secret
GOOGLE_OAUTH_REDIRECT_URI=http://localhost:8000/api/v1/google-drive/callback
GOOGLE_SCOPES=https://www.googleapis.com/auth/drive.file,https://www.googleapis.com/auth/calendar

# Security
FERNET_KEY=chave_fernet_para_encriptacao
FRONTEND_URL=http://localhost:3000
```

4. **Execute as migrações**

O SQLAlchemy criará as tabelas automaticamente na primeira execução:

```bash
poetry run python run.py
```

## ▶️ Como Executar

### Modo de Desenvolvimento

Execute o servidor com hot-reload para desenvolvimento:

```bash
poetry run python run.py
```

Ou diretamente via Uvicorn:

```bash
poetry run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

A API estará acessível em: `http://127.0.0.1:8000`

### Documentação Interativa

Explore e teste a API diretamente pelo navegador:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## ☁️ Integração Google

O sistema possui integração nativa com serviços do Google para potencializar a gestão das equipes:

### 📅 Google Calendar
Cada equipe pode ter seu próprio calendário compartilhado.
- **Eventos de Equipe**: Agende treinos, reuniões e campeonatos.
- **Sincronização**: Eventos criados no sistema aparecem automaticamente no Google Calendar da equipe.

### 📁 Google Drive
Organize documentos e mídias da equipe.
- **Pastas de Equipe**: Criação automática de estrutura de pastas para cada equipe.
- **Upload de Arquivos**: Armazenamento seguro de replays, estratégias e planilhas.

## 📂 Estrutura do Projeto

```
manager-api/
├── app/
│   ├── api/            # Endpoints da API (v1)
│   ├── core/           # Configurações e conexão com DB
│   ├── models/         # Modelos do SQLAlchemy (Tabelas)
│   ├── schemas/        # Schemas do Pydantic (Validação)
│   ├── services/       # Lógica de negócios
│   ├── utils/          # Utilitários (Segurança, etc)
│   └── main.py         # Entrypoint da aplicação
├── .env_example        # Exemplo de variáveis de ambiente
├── pyproject.toml      # Dependências do projeto
└── run.py              # Script de execução
```

## 💻 Tecnologias

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web moderno de alta performance.
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: ORM poderoso para Python.
- **[Pydantic](https://docs.pydantic.dev/)**: Validação de dados robusta.
- **[PostgreSQL](https://www.postgresql.org/)**: Banco de dados relacional confiável.
- **[Poetry](https://python-poetry.org/)**: Gerenciamento de dependências e empacotamento.

## 🔐 Permissões

| Role | Descrição | Permissões |
|------|-----------|------------|
| **Administrador** | Acesso total | Gerenciar tudo: usuários, equipes, inventários e finanças. |
| **Líder** | Gestor de Equipe | Gerenciar sua própria equipe, adicionar membros e ver dados da equipe. |
| **Membro** | Usuário Básico | Visualizar dados da equipe, calendário, arquivos e editar próprio perfil. |

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/MinhaFeature`)
3. Faça o Commit de suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Faça o Push para a Branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

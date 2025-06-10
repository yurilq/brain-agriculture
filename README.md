# 🌾 Brain Agriculture API

API REST desenvolvida com **FastAPI** e **PostgreSQL** para gerenciamento de produtores rurais, fazendas, safras e culturas. A aplicação também oferece um **dashboard gráfico** com dados agregados.

---

## 🧱 Tecnologias Utilizadas

- Python 3.11
- FastAPI
- SQLAlchemy
- Alembic (migrations)
- PostgreSQL
- Docker + Docker Compose
- Chart.js (para visualização de dados no dashboard)
- HTML estático via FastAPI

---

## 🚀 Como Subir o Projeto com Docker

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/brain-agriculture.git
cd brain-agriculture

### 2. Suba os containers (API + Banco de Dados)

docker compose up -d --build

Aguarde até que o container do banco esteja com status healthy.

3. Execute as migrações Alembic

docker compose exec app alembic upgrade head

🧪 Inserindo Dados no Banco
Você pode inserir dados via Swagger UI:

Acesse: http://localhost:8000/docs

Use os endpoints para criar:

Produtores

Fazendas vinculadas a produtores

Culturas

Safras vinculadas a fazendas e culturas

Os dados inseridos alimentarão o dashboard.

📊 Acessando o Dashboard
A aplicação gera gráficos com base nos dados cadastrados.

▶️ Acesse o HTML com gráficos:

http://localhost:8000/static/dashboard_grafico.html
▶️ Ou consuma o JSON direto da API:
bash
Copiar
Editar
http://localhost:8000/dashboard/resumo
O dashboard mostra:

✅ Total de fazendas cadastradas

✅ Total de hectares

✅ Gráfico de pizza por estado

✅ Gráfico de pizza por cultura

✅ Gráfico de uso do solo (área agricultável x vegetação)

📂 Estrutura de Pastas


app/
├── core/              # Conexão com banco de dados
├── models/            # Modelos ORM
├── routes/            # Endpoints
├── schemas/           # Pydantic schemas
├── static/            # HTML do dashboard
└── main.py            # Arquivo principal FastAPI
✅ Checklist de Funcionalidades

 CRUD de produtores

 CRUD de fazendas

 CRUD de culturas

 CRUD de safras

 Validação de CPF/CNPJ

 Validação de área agricultável + vegetação ≤ total

 Dashboard em HTML + JSON

 Registro de logs

 Deploy local com Docker

👨‍💻 Autor
Yuri Lopes Queiroz
Desenvolvedor Backend Python + FastAPI
Contato: yurilq@gmail.com



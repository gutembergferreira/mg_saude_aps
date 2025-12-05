# MG Saúde APS

Plataforma de gestão para Atenção Primária à Saúde (APS), focada em:

- Integração com **e-SUS APS**, CADSUS, CNES e dados financeiros (FNS);
- Cálculo e monitoramento de indicadores de **cofinanciamento federal** (Portaria GM/MS 3.493/2024);
- Dashboards clínicos, epidemiológicos, territoriais e financeiros;
- Suporte a planejamento com matriz GUT e acompanhamento de ações.

## Stack inicial

- Backend: **Python + FastAPI**
- Banco de dados: **PostgreSQL** (camadas staging, DW e app)
- ETL: scripts em Python
- Infra: Docker / docker-compose (dev)

## Estrutura

- `docs/` – visão do produto, arquitetura e modelo de dados (DW)
- `backend/` – API FastAPI e modelos ORM
- `etl/` – pipelines de ingestão e carga para o DW
- `infra/` – arquivos de infraestrutura (Docker, Nginx, etc.)

Este repositório foi preparado para desenvolvimento assistido por IA (Codex) com GitHub.

## Migrações do DW

Para criar o schema e tabelas do Data Warehouse (schema `dw`) em um banco PostgreSQL, configure as variáveis de ambiente de conexão (ver `backend/app/core/config.py`) e execute a partir da raiz do projeto:

```bash
alembic upgrade head
```

## ETL de exemplo (staging → DW)

- CSVs fictícios usados pelos jobs estão em `data/esus_cadastros_example.csv` e `data/esus_atendimentos_example.csv`.
- Ordem sugerida de execução:
  1. `python -m etl.jobs.esus_cadastros_load_stg`
  2. `python -m etl.jobs.esus_atendimentos_load_stg`
  3. `python -m etl.jobs.dw_load_cadastros`
  4. `python -m etl.jobs.dw_load_atendimentos`
- Os jobs usam as credenciais de banco definidas em `etl/config.py` (ou variáveis de ambiente compatíveis).

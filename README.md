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

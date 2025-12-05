# Arquitetura Técnica – MG Saúde APS

## Camadas

1. **Fontes de dados**
   - e-SUS APS
   - CADSUS
   - CNES
   - FNS (dados financeiros)
   - Serviços de mapas (WMS/WFS, OSM, etc.)

2. **Ingestão / ETL**
   - Scripts Python (jobs em `etl/jobs/`)
   - Área de staging em PostgreSQL (schemas `stg`)

3. **Data Warehouse (DW)**
   - Schema `dw` em PostgreSQL
   - Tabelas dimensão: tempo, município, unidade, equipe, território, paciente, indicador
   - Tabelas fato: cadastros APS, atendimentos, indicadores, financeiro, ações

4. **API / Backend**
   - FastAPI em `backend/app/`
   - ORM SQLAlchemy acessando o DW
   - Endpoints para indicadores, painéis clínicos, planejamento, etc.

5. **Dashboards / Frontend**
   - A definir (pode ser integração com BI ou front próprio)

6. **Infra**
   - Docker / docker-compose (desenvolvimento)
   - Nginx como proxy reverso (produção)

Este documento é o contexto principal para o agente de código (Codex).

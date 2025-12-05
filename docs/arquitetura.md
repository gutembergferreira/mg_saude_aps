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

## Geoprocessamento

- A API expõe dados georreferenciados de unidades e territórios para consumo por mapas/BI.
- Endpoints:
  - `/api/v1/geo/unidades/{codigo_ibge_municipio}`: retorna unidades com latitude/longitude e contagem de cadastros e atendimentos (12 meses).
  - `/api/v1/geo/indicador/{codigo_ibge_municipio}`: heatmap de indicadores por `nivel=unidade` (default) ou `nivel=territorio`, filtrando por `indicador` e `periodo`.
- As dimensões `dw.dim_unidade_saude` e `dw.dim_territorio` possuem colunas opcionais de latitude/longitude (NUMERIC) usadas na resposta.

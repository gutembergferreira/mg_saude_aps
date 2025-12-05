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

## API de Indicadores APS

Endpoint principal:

- `GET /api/v1/indicadores/{codigo_ibge_municipio}`
  - Query params opcionais: `indicador` (ex.: C1, C2) e `periodo` (ex.: 2025Q1, 2025M03).
  - Resposta exemplo:
    ```json
    [
      {
        "municipio": "Recife",
        "codigo_ibge": "2611606",
        "indicador": "C1",
        "nome_indicador": "Nome amigável",
        "periodo_referencia": "2025Q1",
        "valor": 0.85,
        "meta": 0.8,
        "atingiu_meta": true
      }
    ]
    ```

## API de Painéis Clínicos

Endpoints iniciais para dashboards:

- `GET /api/v1/painel/gestantes/{codigo_ibge_municipio}`: lista gestantes (sexo F) com atendimentos dos últimos 12 meses, filtros opcionais `unidade` (CNES) e `equipe`.
- `GET /api/v1/painel/criancas/{codigo_ibge_municipio}`: lista crianças (faixas 0-1, 1-4) com atendimentos dos últimos 12 meses, filtros opcionais `unidade`, `equipe`, `faixa_etaria`.
- Uso típico para BI/front: consumir a lista e montar cartões/indicadores (contagem, último atendimento etc.).

## Planejamento (Matriz GUT)

- Tabelas de aplicação `app_problema_gut` e `app_acao_planejada` para registrar problemas priorizados e ações.
- Endpoints principais:
  - `POST /api/v1/planejamento/problemas` (criar), `GET /api/v1/planejamento/problemas` (listar por município/código IBGE, filtrar por status)
  - `GET /api/v1/planejamento/problemas/{id}`, `PATCH /api/v1/planejamento/problemas/{id}`
  - `POST /api/v1/planejamento/acoes`, `GET /api/v1/planejamento/acoes/{problema_id}`, `PATCH /api/v1/planejamento/acoes/{acao_id}`
- Score GUT calculado como `gravidade * urgencia * tendencia`.

## Geoprocessamento

- `GET /api/v1/geo/unidades/{codigo_ibge_municipio}`: unidades de saúde com latitude/longitude e contagens (cadastros e atendimentos nos últimos 12 meses).
- `GET /api/v1/geo/indicador/{codigo_ibge_municipio}?indicador=C1&periodo=2025Q1&nivel=unidade|territorio`: valores de indicadores agregados para mapa/heatmap.
- Dimensões `dw.dim_unidade_saude` e `dw.dim_territorio` possuem campos opcionais `latitude`/`longitude` usados nas respostas.

## Observabilidade

- Logging padronizado com Loguru (formato com timestamp, nível e módulo), middleware de requisições com tempo de resposta.
- Health checks:
  - `/health` simples.
  - `/health/details` verifica conectividade com o banco e retorna latência.
- Métricas iniciais:
  - `/metrics` retorna contadores em texto (requests_total, errors_total), base para futura integração Prometheus/Grafana.

## Seed de dados (demo/PoC)

1. Garanta o banco ativo (docker-compose) e rode as migrações:
   ```bash
   alembic upgrade head
   ```
2. Execute os seeds:
   ```bash
   python -m backend.app.seed.run_all_seeds
   ```
3. Dados criados:
   - Municípios: Recife (2611606), Manaus (1302603), Belo Horizonte (3106200)
   - Indicadores: C1–C7 (descrições simplificadas)
   - Usuários (senha `Senha123!`):
     - admin@mgsaude.local (perfil admin)
     - gestor.recife@mgsaude.local (perfil gestor_municipal, Recife)
     - profissional.recife@mgsaude.local (perfil profissional, Recife)
   - Dados demo: pacientes, cadastros/atendimentos e indicadores para Recife (períodos 2025Q1/Q2) para alimentar indicadores, painéis e geo.

## Ambiente de DEMO (Docker)

1. Copie o `.env.example` para `.env` e ajuste se necessário.
2. Suba os serviços (Postgres, backend, nginx e etl):
   ```bash
   cd infra
   docker-compose up --build
   ```
3. Acesse a API via Nginx: `http://localhost/health` (ou `/api/...`).
4. (Opcional) rode os seeds dentro do contêiner backend:
   ```bash
   docker exec -it mg_saude_backend bash -lc "alembic upgrade head && python -m backend.app.seed.run_all_seeds"
   ```

## ETL de exemplo (staging → DW)

- CSVs fictícios usados pelos jobs estão em `data/esus_cadastros_example.csv` e `data/esus_atendimentos_example.csv`.
- Ordem sugerida de execução:
  1. `python -m etl.jobs.esus_cadastros_load_stg`
  2. `python -m etl.jobs.esus_atendimentos_load_stg`
  3. `python -m etl.jobs.dw_load_cadastros`
  4. `python -m etl.jobs.dw_load_atendimentos`
- Os jobs usam as credenciais de banco definidas em `etl/config.py` (ou variáveis de ambiente compatíveis).

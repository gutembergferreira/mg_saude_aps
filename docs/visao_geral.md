# Visão Geral – MG Saúde APS

A MG Saúde APS é uma plataforma de gestão para Atenção Primária à Saúde que:

- Integra dados do **e-SUS APS** (centralizador / prontuário), **CADSUS**, **CNES** e **FNS**;
- Estrutura um **Data Warehouse (DW)** próprio para consultas analíticas;
- Calcula e exibe indicadores de **cofinanciamento** conforme Portaria GM/MS 3.493/2024;
- Oferece painéis clínicos (gestantes, crianças, crônicos), epidemiológicos, financeiros e territoriais (geoprocessamento);
- Suporta planejamento com **Matriz GUT** e monitoramento de ações.

A arquitetura geral é:

Fontes (e-SUS APS, CADSUS, CNES, FNS) → ETL (staging) → DW (PostgreSQL) → API (FastAPI) → Dashboards / Frontend / BI.

# Performance e índices

Consultas críticas:
- Indicadores (`/api/v1/indicadores/{codigo_ibge_municipio}`): filtro por município, indicador e período.
- Painéis clínicos (gestantes/crianças): filtro por município, últimos 12 meses.
- Geoprocessamento: agregações por unidade/território, filtros por município e período.

Índices adicionados (migração 20240901_0006):
- `dw.fato_indicador_aps`: (`id_municipio`, `id_indicador`, `periodo_referencia`) – `ix_fato_indicador_mun_ind_per`
- `dw.fato_atendimento_aps`: (`id_municipio`, `id_unidade`, `id_equipe`, `id_paciente`, `id_tempo`) – `ix_fato_atendimento_mun_unid_equipe_paciente_tempo`
- `dw.dim_paciente`: (`hash_identificador`, `id_municipio`) – `ix_dim_paciente_hash_municipio`

Estratégia de consultas:
- Aplicar filtros por município/indicador/período antes de agregações.
- Medir tempo de execução nos services críticos com logs `[PERF]`.

Futuros passos:
- Avaliar views materializadas para indicadores por município/unidade/período conforme volume crescer.

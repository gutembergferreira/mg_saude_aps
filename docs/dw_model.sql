CREATE SCHEMA IF NOT EXISTS dw;

CREATE TABLE dw.dim_tempo (
    id_tempo          SERIAL PRIMARY KEY,
    data              DATE NOT NULL UNIQUE,
    ano               INTEGER NOT NULL,
    mes               INTEGER NOT NULL,
    dia               INTEGER NOT NULL,
    trimestre         INTEGER NOT NULL,
    quadrimestre      INTEGER NOT NULL,
    nome_mes          VARCHAR(20) NOT NULL,
    nome_dia_semana   VARCHAR(20) NOT NULL,
    eh_final_semana   BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE dw.dim_municipio (
    id_municipio      SERIAL PRIMARY KEY,
    codigo_ibge       VARCHAR(7) NOT NULL UNIQUE,
    nome              VARCHAR(100) NOT NULL,
    uf                CHAR(2) NOT NULL,
    regional_saude    VARCHAR(100),
    populacao_estim   INTEGER
);

CREATE TABLE dw.dim_unidade_saude (
    id_unidade        SERIAL PRIMARY KEY,
    codigo_cnes       VARCHAR(15) NOT NULL,
    nome              VARCHAR(150) NOT NULL,
    tipo_unidade      VARCHAR(50),
    id_municipio      INTEGER NOT NULL REFERENCES dw.dim_municipio(id_municipio)
);

CREATE TABLE dw.dim_equipe (
    id_equipe         SERIAL PRIMARY KEY,
    codigo_equipe     VARCHAR(50) NOT NULL,
    tipo_equipe       VARCHAR(50),
    descricao         VARCHAR(150),
    id_unidade        INTEGER NOT NULL REFERENCES dw.dim_unidade_saude(id_unidade)
);

CREATE TABLE dw.dim_profissional (
    id_profissional   SERIAL PRIMARY KEY,
    cbo               VARCHAR(10),
    nome_abreviado    VARCHAR(100),
    conselho_classe   VARCHAR(20),
    numero_registro   VARCHAR(30)
);

CREATE TABLE dw.dim_territorio (
    id_territorio     SERIAL PRIMARY KEY,
    codigo_territorio VARCHAR(50) NOT NULL,
    descricao         VARCHAR(150),
    id_equipe         INTEGER REFERENCES dw.dim_equipe(id_equipe)
);

CREATE TABLE dw.dim_paciente (
    id_paciente       BIGSERIAL PRIMARY KEY,
    id_municipio      INTEGER NOT NULL REFERENCES dw.dim_municipio(id_municipio),
    sexo              CHAR(1),
    data_nascimento   DATE,
    faixa_etaria      VARCHAR(20),
    hash_identificador VARCHAR(128)
);

CREATE TABLE dw.dim_indicador (
    id_indicador      SERIAL PRIMARY KEY,
    codigo            VARCHAR(20) NOT NULL,
    nome              VARCHAR(150) NOT NULL,
    descricao         TEXT,
    tipo              VARCHAR(50),
    fonte_metodologia VARCHAR(200)
);

CREATE TABLE dw.fato_cadastro_aps (
    id_fato_cad       BIGSERIAL PRIMARY KEY,
    id_tempo          INTEGER NOT NULL REFERENCES dw.dim_tempo(id_tempo),
    id_municipio      INTEGER NOT NULL REFERENCES dw.dim_municipio(id_municipio),
    id_unidade        INTEGER REFERENCES dw.dim_unidade_saude(id_unidade),
    id_equipe         INTEGER REFERENCES dw.dim_equipe(id_equipe),
    id_paciente       BIGINT REFERENCES dw.dim_paciente(id_paciente),
    id_territorio     INTEGER REFERENCES dw.dim_territorio(id_territorio),
    cadastro_valido   BOOLEAN NOT NULL,
    eh_publico_alvo   BOOLEAN NOT NULL,
    peso_capitacao    NUMERIC(10,4)
);

CREATE TABLE dw.fato_atendimento_aps (
    id_fato_atend     BIGSERIAL PRIMARY KEY,
    id_tempo          INTEGER NOT NULL REFERENCES dw.dim_tempo(id_tempo),
    id_municipio      INTEGER NOT NULL REFERENCES dw.dim_municipio(id_municipio),
    id_unidade        INTEGER REFERENCES dw.dim_unidade_saude(id_unidade),
    id_equipe         INTEGER REFERENCES dw.dim_equipe(id_equipe),
    id_profissional   INTEGER REFERENCES dw.dim_profissional(id_profissional),
    id_paciente       BIGINT REFERENCES dw.dim_paciente(id_paciente),
    id_territorio     INTEGER REFERENCES dw.dim_territorio(id_territorio),
    tipo_atendimento  VARCHAR(50),
    codigo_proced     VARCHAR(20),
    quantidade        NUMERIC(10,2) DEFAULT 1,
    local_atendimento VARCHAR(50),
    origem_dado       VARCHAR(50)
);

CREATE TABLE dw.fato_indicador_aps (
    id_fato_ind       BIGSERIAL PRIMARY KEY,
    id_tempo          INTEGER NOT NULL REFERENCES dw.dim_tempo(id_tempo),
    id_municipio      INTEGER NOT NULL REFERENCES dw.dim_municipio(id_municipio),
    id_unidade        INTEGER REFERENCES dw.dim_unidade_saude(id_unidade),
    id_equipe         INTEGER REFERENCES dw.dim_equipe(id_equipe),
    id_territorio     INTEGER REFERENCES dw.dim_territorio(id_territorio),
    id_indicador      INTEGER NOT NULL REFERENCES dw.dim_indicador(id_indicador),
    periodo_referencia VARCHAR(10) NOT NULL,
    numerador          NUMERIC(18,4),
    denominador        NUMERIC(18,4),
    valor              NUMERIC(18,4),
    meta               NUMERIC(18,4),
    atingiu_meta       BOOLEAN
);

CREATE TABLE dw.fato_financeiro_aps (
    id_fato_fin       BIGSERIAL PRIMARY KEY,
    id_tempo          INTEGER NOT NULL REFERENCES dw.dim_tempo(id_tempo),
    id_municipio      INTEGER NOT NULL REFERENCES dw.dim_municipio(id_municipio),
    tipo_recurso      VARCHAR(50),
    programa          VARCHAR(100),
    valor_creditado   NUMERIC(18,2),
    competencia_ref   VARCHAR(7),
    origem_dado       VARCHAR(50)
);

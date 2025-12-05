CREATE SCHEMA IF NOT EXISTS stg;

CREATE TABLE IF NOT EXISTS stg.stg_esus_cadastros (
    id_cadastro             SERIAL PRIMARY KEY,
    codigo_ibge_municipio   VARCHAR(7) NOT NULL,
    data_cadastro           DATE NOT NULL,
    sexo                    CHAR(1),
    data_nascimento         DATE,
    hash_identificador      VARCHAR(128),
    codigo_unidade          VARCHAR(15),
    codigo_equipe           VARCHAR(50),
    codigo_territorio       VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS stg.stg_esus_atendimentos (
    id_atendimento              SERIAL PRIMARY KEY,
    codigo_ibge_municipio       VARCHAR(7) NOT NULL,
    data_atendimento            DATE NOT NULL,
    codigo_unidade              VARCHAR(15),
    codigo_equipe               VARCHAR(50),
    cbo_profissional            VARCHAR(10),
    hash_identificador_paciente VARCHAR(128),
    tipo_atendimento            VARCHAR(50),
    codigo_proced               VARCHAR(20),
    quantidade                  NUMERIC(10,2) DEFAULT 1,
    codigo_territorio           VARCHAR(50)
);

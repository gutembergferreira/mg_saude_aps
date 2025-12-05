from datetime import date
from typing import Optional, Tuple

from etl.utils.db import get_connection
from etl.utils.logging import configure_etl_logging, get_logger

logger = get_logger()


def _ensure_tempo(cur, data_ref: date) -> int:
    cur.execute("SELECT id_tempo FROM dw.dim_tempo WHERE data = %s", (data_ref,))
    row = cur.fetchone()
    if row:
        return row[0]

    ano = data_ref.year
    mes = data_ref.month
    dia = data_ref.day
    trimestre = (mes - 1) // 3 + 1
    quadrimestre = (mes - 1) // 4 + 1
    nome_mes = data_ref.strftime("%B")
    nome_dia_semana = data_ref.strftime("%A")
    eh_final_semana = data_ref.weekday() >= 5

    cur.execute(
        """
        INSERT INTO dw.dim_tempo (
            data, ano, mes, dia, trimestre, quadrimestre,
            nome_mes, nome_dia_semana, eh_final_semana
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id_tempo
        """,
        (data_ref, ano, mes, dia, trimestre, quadrimestre, nome_mes, nome_dia_semana, eh_final_semana),
    )
    return cur.fetchone()[0]


def _ensure_municipio(cur, codigo_ibge: str) -> int:
    cur.execute("SELECT id_municipio FROM dw.dim_municipio WHERE codigo_ibge = %s", (codigo_ibge,))
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        """
        INSERT INTO dw.dim_municipio (codigo_ibge, nome, uf)
        VALUES (%s, %s, %s)
        RETURNING id_municipio
        """,
        (codigo_ibge, f"Municipio {codigo_ibge}", "NA"),
    )
    return cur.fetchone()[0]


def _ensure_unidade(cur, codigo_unidade: Optional[str], id_municipio: int) -> Optional[int]:
    if not codigo_unidade:
        return None
    cur.execute(
        "SELECT id_unidade FROM dw.dim_unidade_saude WHERE codigo_cnes = %s AND id_municipio = %s",
        (codigo_unidade, id_municipio),
    )
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        """
        INSERT INTO dw.dim_unidade_saude (codigo_cnes, nome, id_municipio)
        VALUES (%s, %s, %s)
        RETURNING id_unidade
        """,
        (codigo_unidade, f"Unidade {codigo_unidade}", id_municipio),
    )
    return cur.fetchone()[0]


def _ensure_equipe(cur, codigo_equipe: Optional[str], id_unidade: Optional[int]) -> Optional[int]:
    if not codigo_equipe or id_unidade is None:
        return None
    cur.execute(
        "SELECT id_equipe FROM dw.dim_equipe WHERE codigo_equipe = %s AND id_unidade = %s",
        (codigo_equipe, id_unidade),
    )
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        """
        INSERT INTO dw.dim_equipe (codigo_equipe, id_unidade)
        VALUES (%s, %s)
        RETURNING id_equipe
        """,
        (codigo_equipe, id_unidade),
    )
    return cur.fetchone()[0]


def _ensure_territorio(cur, codigo_territorio: Optional[str], id_equipe: Optional[int]) -> Optional[int]:
    if not codigo_territorio or id_equipe is None:
        return None
    cur.execute(
        "SELECT id_territorio FROM dw.dim_territorio WHERE codigo_territorio = %s AND id_equipe = %s",
        (codigo_territorio, id_equipe),
    )
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        """
        INSERT INTO dw.dim_territorio (codigo_territorio, id_equipe)
        VALUES (%s, %s)
        RETURNING id_territorio
        """,
        (codigo_territorio, id_equipe),
    )
    return cur.fetchone()[0]


def _ensure_paciente(
    cur,
    id_municipio: int,
    sexo: Optional[str],
    data_nascimento: Optional[date],
    hash_identificador: Optional[str],
) -> int:
    cur.execute(
        """
        SELECT id_paciente
        FROM dw.dim_paciente
        WHERE hash_identificador = %s AND id_municipio = %s
        """,
        (hash_identificador, id_municipio),
    )
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        """
        INSERT INTO dw.dim_paciente (id_municipio, sexo, data_nascimento, hash_identificador)
        VALUES (%s, %s, %s, %s)
        RETURNING id_paciente
        """,
        (id_municipio, sexo, data_nascimento, hash_identificador),
    )
    return cur.fetchone()[0]


def _resolve_ids(cur, stg_row: Tuple) -> dict:
    (
        codigo_ibge_municipio,
        data_cadastro,
        sexo,
        data_nascimento,
        hash_identificador,
        codigo_unidade,
        codigo_equipe,
        codigo_territorio,
    ) = stg_row

    id_tempo = _ensure_tempo(cur, data_cadastro)
    id_municipio = _ensure_municipio(cur, codigo_ibge_municipio)
    id_unidade = _ensure_unidade(cur, codigo_unidade, id_municipio)
    id_equipe = _ensure_equipe(cur, codigo_equipe, id_unidade)
    id_territorio = _ensure_territorio(cur, codigo_territorio, id_equipe)
    id_paciente = _ensure_paciente(cur, id_municipio, sexo, data_nascimento, hash_identificador)

    return {
        "id_tempo": id_tempo,
        "id_municipio": id_municipio,
        "id_unidade": id_unidade,
        "id_equipe": id_equipe,
        "id_territorio": id_territorio,
        "id_paciente": id_paciente,
    }


def load_dw_from_cadastros():
    logger.info("[ETL] job=dw_load_cadastros start")
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            codigo_ibge_municipio,
            data_cadastro,
            sexo,
            data_nascimento,
            hash_identificador,
            codigo_unidade,
            codigo_equipe,
            codigo_territorio
        FROM stg.stg_esus_cadastros
        ORDER BY id_cadastro
        """
    )
    rows = cur.fetchall()
    if not rows:
        logger.warning("[ETL] job=dw_load_cadastros no_rows")
        cur.close()
        conn.close()
        return 0

    inserted = 0
    for stg_row in rows:
        ids = _resolve_ids(cur, stg_row)
        cur.execute(
            """
            INSERT INTO dw.fato_cadastro_aps (
                id_tempo, id_municipio, id_unidade, id_equipe,
                id_paciente, id_territorio, cadastro_valido,
                eh_publico_alvo, peso_capitacao
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                ids["id_tempo"],
                ids["id_municipio"],
                ids["id_unidade"],
                ids["id_equipe"],
                ids["id_paciente"],
                ids["id_territorio"],
                True,
                True,
                1.0,
            ),
        )
        inserted += 1

    conn.commit()
    cur.close()
    conn.close()
    logger.info("[ETL] job=dw_load_cadastros records_inserted={}", inserted)
    return inserted


if __name__ == "__main__":
    configure_etl_logging()
    load_dw_from_cadastros()

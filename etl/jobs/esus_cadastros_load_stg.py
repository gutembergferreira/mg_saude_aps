import csv
from datetime import date
from pathlib import Path
from typing import List, Tuple

from etl.utils.db import get_connection
from etl.utils.logging import configure_etl_logging, get_logger

logger = get_logger()


def _parse_date(value: str) -> date:
    return date.fromisoformat(value) if value else None


def _load_rows(csv_path: Path) -> List[Tuple]:
    rows: List[Tuple] = []
    with csv_path.open(newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for raw in reader:
            rows.append(
                (
                    raw.get("codigo_ibge_municipio"),
                    _parse_date(raw.get("data_cadastro") or ""),
                    (raw.get("sexo") or "").upper()[:1] or None,
                    _parse_date(raw.get("data_nascimento") or ""),
                    raw.get("hash_identificador") or None,
                    raw.get("codigo_unidade") or None,
                    raw.get("codigo_equipe") or None,
                    raw.get("codigo_territorio") or None,
                )
            )
    return rows


def load_cadastros_to_stg(csv_path: Path) -> int:
    logger.info("[ETL] job=esus_cadastros_load_stg start path={}", csv_path)
    rows = _load_rows(csv_path)
    if not rows:
        logger.warning("[ETL] job=esus_cadastros_load_stg no_rows path={}", csv_path)
        return 0

    conn = get_connection()
    cur = conn.cursor()
    cur.executemany(
        """
        INSERT INTO stg.stg_esus_cadastros (
            codigo_ibge_municipio, data_cadastro, sexo, data_nascimento,
            hash_identificador, codigo_unidade, codigo_equipe, codigo_territorio
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        rows,
    )
    conn.commit()
    cur.close()
    conn.close()
    logger.info("[ETL] job=esus_cadastros_load_stg records_inserted={}", len(rows))
    return len(rows)


if __name__ == "__main__":
    configure_etl_logging()
    default_path = Path(__file__).resolve().parents[2] / "data" / "esus_cadastros_example.csv"
    load_cadastros_to_stg(default_path)

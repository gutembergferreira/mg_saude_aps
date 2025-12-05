from datetime import date, timedelta

from etl.utils.db import get_connection


def popular_dim_tempo(data_inicio: date, data_fim: date):
    conn = get_connection()
    cur = conn.cursor()

    data_atual = data_inicio
    while data_atual <= data_fim:
        ano = data_atual.year
        mes = data_atual.month
        dia = data_atual.day
        trimestre = (mes - 1) // 3 + 1
        quadrimestre = (mes - 1) // 4 + 1
        nome_mes = data_atual.strftime("%B")
        nome_dia_semana = data_atual.strftime("%A")
        eh_final_semana = data_atual.weekday() >= 5

        cur.execute(
            """
            INSERT INTO dw.dim_tempo (
                data, ano, mes, dia, trimestre, quadrimestre,
                nome_mes, nome_dia_semana, eh_final_semana
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (data) DO NOTHING
            """,
            (
                data_atual,
                ano,
                mes,
                dia,
                trimestre,
                quadrimestre,
                nome_mes,
                nome_dia_semana,
                eh_final_semana,
            ),
        )

        data_atual += timedelta(days=1)

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    popular_dim_tempo(date(2015, 1, 1), date(2030, 12, 31))

"""add performance indexes

Revision ID: 20240901_0006
Revises: 20240901_0005
Create Date: 2024-09-01 05:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20240901_0006"
down_revision = "20240901_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(
        "ix_fato_indicador_mun_ind_per",
        "fato_indicador_aps",
        ["id_municipio", "id_indicador", "periodo_referencia"],
        unique=False,
        schema="dw",
    )
    op.create_index(
        "ix_fato_atendimento_mun_unid_equipe_paciente_tempo",
        "fato_atendimento_aps",
        ["id_municipio", "id_unidade", "id_equipe", "id_paciente", "id_tempo"],
        unique=False,
        schema="dw",
    )
    op.create_index(
        "ix_dim_paciente_hash_municipio",
        "dim_paciente",
        ["hash_identificador", "id_municipio"],
        unique=False,
        schema="dw",
    )


def downgrade() -> None:
    op.drop_index("ix_dim_paciente_hash_municipio", table_name="dim_paciente", schema="dw")
    op.drop_index("ix_fato_atendimento_mun_unid_equipe_paciente_tempo", table_name="fato_atendimento_aps", schema="dw")
    op.drop_index("ix_fato_indicador_mun_ind_per", table_name="fato_indicador_aps", schema="dw")

"""create stg schema and staging tables for e-SUS APS

Revision ID: 20240901_0002
Revises: 20240901_0001
Create Date: 2024-09-01 01:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20240901_0002"
down_revision = "20240901_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS stg")

    op.create_table(
        "stg_esus_cadastros",
        sa.Column("id_cadastro", sa.Integer(), primary_key=True),
        sa.Column("codigo_ibge_municipio", sa.String(length=7), nullable=False),
        sa.Column("data_cadastro", sa.Date(), nullable=False),
        sa.Column("sexo", sa.String(length=1)),
        sa.Column("data_nascimento", sa.Date()),
        sa.Column("hash_identificador", sa.String(length=128)),
        sa.Column("codigo_unidade", sa.String(length=15)),
        sa.Column("codigo_equipe", sa.String(length=50)),
        sa.Column("codigo_territorio", sa.String(length=50)),
        schema="stg",
    )

    op.create_table(
        "stg_esus_atendimentos",
        sa.Column("id_atendimento", sa.Integer(), primary_key=True),
        sa.Column("codigo_ibge_municipio", sa.String(length=7), nullable=False),
        sa.Column("data_atendimento", sa.Date(), nullable=False),
        sa.Column("codigo_unidade", sa.String(length=15)),
        sa.Column("codigo_equipe", sa.String(length=50)),
        sa.Column("cbo_profissional", sa.String(length=10)),
        sa.Column("hash_identificador_paciente", sa.String(length=128)),
        sa.Column("tipo_atendimento", sa.String(length=50)),
        sa.Column("codigo_proced", sa.String(length=20)),
        sa.Column("quantidade", sa.Numeric(10, 2), server_default=sa.text("1")),
        sa.Column("codigo_territorio", sa.String(length=50)),
        schema="stg",
    )


def downgrade() -> None:
    op.drop_table("stg_esus_atendimentos", schema="stg")
    op.drop_table("stg_esus_cadastros", schema="stg")
    op.execute("DROP SCHEMA IF EXISTS stg")

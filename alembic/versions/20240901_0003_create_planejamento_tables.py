"""create planejamento tables

Revision ID: 20240901_0003
Revises: 20240901_0002
Create Date: 2024-09-01 02:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20240901_0003"
down_revision = "20240901_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "app_problema_gut",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("id_municipio", sa.Integer(), sa.ForeignKey("dw.dim_municipio.id_municipio"), nullable=False),
        sa.Column("id_unidade", sa.Integer(), sa.ForeignKey("dw.dim_unidade_saude.id_unidade")),
        sa.Column("id_equipe", sa.Integer(), sa.ForeignKey("dw.dim_equipe.id_equipe")),
        sa.Column("titulo", sa.String(length=255), nullable=False),
        sa.Column("descricao", sa.Text()),
        sa.Column("gravidade", sa.Integer(), nullable=False),
        sa.Column("urgencia", sa.Integer(), nullable=False),
        sa.Column("tendencia", sa.Integer(), nullable=False),
        sa.Column("score_gut", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="planejado"),
        sa.Column("data_criacao", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("data_ultima_atualizacao", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("criado_por", sa.String(length=100)),
    )

    op.create_table(
        "app_acao_planejada",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("problema_id", sa.Integer(), sa.ForeignKey("app_problema_gut.id"), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=False),
        sa.Column("responsavel", sa.String(length=100)),
        sa.Column("data_inicio_prevista", sa.Date()),
        sa.Column("data_fim_prevista", sa.Date()),
        sa.Column("data_inicio_real", sa.Date()),
        sa.Column("data_fim_real", sa.Date()),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="planejada"),
        sa.Column("observacoes", sa.Text()),
    )


def downgrade() -> None:
    op.drop_table("app_acao_planejada")
    op.drop_table("app_problema_gut")

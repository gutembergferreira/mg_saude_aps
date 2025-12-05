"""create dw schema and tables

Revision ID: 20240901_0001
Revises: 
Create Date: 2024-09-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20240901_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS dw")

    op.create_table(
        "dim_tempo",
        sa.Column("id_tempo", sa.Integer(), primary_key=True),
        sa.Column("data", sa.Date(), nullable=False, unique=True),
        sa.Column("ano", sa.Integer(), nullable=False),
        sa.Column("mes", sa.Integer(), nullable=False),
        sa.Column("dia", sa.Integer(), nullable=False),
        sa.Column("trimestre", sa.Integer(), nullable=False),
        sa.Column("quadrimestre", sa.Integer(), nullable=False),
        sa.Column("nome_mes", sa.String(length=20), nullable=False),
        sa.Column("nome_dia_semana", sa.String(length=20), nullable=False),
        sa.Column("eh_final_semana", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        schema="dw",
    )

    op.create_table(
        "dim_municipio",
        sa.Column("id_municipio", sa.Integer(), primary_key=True),
        sa.Column("codigo_ibge", sa.String(length=7), nullable=False, unique=True),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("uf", sa.String(length=2), nullable=False),
        sa.Column("regional_saude", sa.String(length=100)),
        sa.Column("populacao_estim", sa.Integer()),
        schema="dw",
    )

    op.create_table(
        "dim_unidade_saude",
        sa.Column("id_unidade", sa.Integer(), primary_key=True),
        sa.Column("codigo_cnes", sa.String(length=15), nullable=False),
        sa.Column("nome", sa.String(length=150), nullable=False),
        sa.Column("tipo_unidade", sa.String(length=50)),
        sa.Column("id_municipio", sa.Integer(), sa.ForeignKey("dw.dim_municipio.id_municipio"), nullable=False),
        schema="dw",
    )

    op.create_table(
        "dim_equipe",
        sa.Column("id_equipe", sa.Integer(), primary_key=True),
        sa.Column("codigo_equipe", sa.String(length=50), nullable=False),
        sa.Column("tipo_equipe", sa.String(length=50)),
        sa.Column("descricao", sa.String(length=150)),
        sa.Column("id_unidade", sa.Integer(), sa.ForeignKey("dw.dim_unidade_saude.id_unidade"), nullable=False),
        schema="dw",
    )

    op.create_table(
        "dim_profissional",
        sa.Column("id_profissional", sa.Integer(), primary_key=True),
        sa.Column("cbo", sa.String(length=10)),
        sa.Column("nome_abreviado", sa.String(length=100)),
        sa.Column("conselho_classe", sa.String(length=20)),
        sa.Column("numero_registro", sa.String(length=30)),
        schema="dw",
    )

    op.create_table(
        "dim_territorio",
        sa.Column("id_territorio", sa.Integer(), primary_key=True),
        sa.Column("codigo_territorio", sa.String(length=50), nullable=False),
        sa.Column("descricao", sa.String(length=150)),
        sa.Column("id_equipe", sa.Integer(), sa.ForeignKey("dw.dim_equipe.id_equipe")),
        schema="dw",
    )

    op.create_table(
        "dim_paciente",
        sa.Column("id_paciente", sa.BigInteger(), primary_key=True),
        sa.Column("id_municipio", sa.Integer(), sa.ForeignKey("dw.dim_municipio.id_municipio"), nullable=False),
        sa.Column("sexo", sa.String(length=1)),
        sa.Column("data_nascimento", sa.Date()),
        sa.Column("faixa_etaria", sa.String(length=20)),
        sa.Column("hash_identificador", sa.String(length=128)),
        schema="dw",
    )

    op.create_table(
        "dim_indicador",
        sa.Column("id_indicador", sa.Integer(), primary_key=True),
        sa.Column("codigo", sa.String(length=20), nullable=False),
        sa.Column("nome", sa.String(length=150), nullable=False),
        sa.Column("descricao", sa.Text()),
        sa.Column("tipo", sa.String(length=50)),
        sa.Column("fonte_metodologia", sa.String(length=200)),
        schema="dw",
    )

    op.create_table(
        "fato_cadastro_aps",
        sa.Column("id_fato_cad", sa.BigInteger(), primary_key=True),
        sa.Column("id_tempo", sa.Integer(), sa.ForeignKey("dw.dim_tempo.id_tempo"), nullable=False),
        sa.Column("id_municipio", sa.Integer(), sa.ForeignKey("dw.dim_municipio.id_municipio"), nullable=False),
        sa.Column("id_unidade", sa.Integer(), sa.ForeignKey("dw.dim_unidade_saude.id_unidade")),
        sa.Column("id_equipe", sa.Integer(), sa.ForeignKey("dw.dim_equipe.id_equipe")),
        sa.Column("id_paciente", sa.BigInteger(), sa.ForeignKey("dw.dim_paciente.id_paciente")),
        sa.Column("id_territorio", sa.Integer(), sa.ForeignKey("dw.dim_territorio.id_territorio")),
        sa.Column("cadastro_valido", sa.Boolean(), nullable=False),
        sa.Column("eh_publico_alvo", sa.Boolean(), nullable=False),
        sa.Column("peso_capitacao", sa.Numeric(10, 4)),
        schema="dw",
    )

    op.create_table(
        "fato_atendimento_aps",
        sa.Column("id_fato_atend", sa.BigInteger(), primary_key=True),
        sa.Column("id_tempo", sa.Integer(), sa.ForeignKey("dw.dim_tempo.id_tempo"), nullable=False),
        sa.Column("id_municipio", sa.Integer(), sa.ForeignKey("dw.dim_municipio.id_municipio"), nullable=False),
        sa.Column("id_unidade", sa.Integer(), sa.ForeignKey("dw.dim_unidade_saude.id_unidade")),
        sa.Column("id_equipe", sa.Integer(), sa.ForeignKey("dw.dim_equipe.id_equipe")),
        sa.Column("id_profissional", sa.Integer(), sa.ForeignKey("dw.dim_profissional.id_profissional")),
        sa.Column("id_paciente", sa.BigInteger(), sa.ForeignKey("dw.dim_paciente.id_paciente")),
        sa.Column("id_territorio", sa.Integer(), sa.ForeignKey("dw.dim_territorio.id_territorio")),
        sa.Column("tipo_atendimento", sa.String(length=50)),
        sa.Column("codigo_proced", sa.String(length=20)),
        sa.Column("quantidade", sa.Numeric(10, 2), server_default=sa.text("1")),
        sa.Column("local_atendimento", sa.String(length=50)),
        sa.Column("origem_dado", sa.String(length=50)),
        schema="dw",
    )

    op.create_table(
        "fato_indicador_aps",
        sa.Column("id_fato_ind", sa.BigInteger(), primary_key=True),
        sa.Column("id_tempo", sa.Integer(), sa.ForeignKey("dw.dim_tempo.id_tempo"), nullable=False),
        sa.Column("id_municipio", sa.Integer(), sa.ForeignKey("dw.dim_municipio.id_municipio"), nullable=False),
        sa.Column("id_unidade", sa.Integer(), sa.ForeignKey("dw.dim_unidade_saude.id_unidade")),
        sa.Column("id_equipe", sa.Integer(), sa.ForeignKey("dw.dim_equipe.id_equipe")),
        sa.Column("id_territorio", sa.Integer(), sa.ForeignKey("dw.dim_territorio.id_territorio")),
        sa.Column("id_indicador", sa.Integer(), sa.ForeignKey("dw.dim_indicador.id_indicador"), nullable=False),
        sa.Column("periodo_referencia", sa.String(length=10), nullable=False),
        sa.Column("numerador", sa.Numeric(18, 4)),
        sa.Column("denominador", sa.Numeric(18, 4)),
        sa.Column("valor", sa.Numeric(18, 4)),
        sa.Column("meta", sa.Numeric(18, 4)),
        sa.Column("atingiu_meta", sa.Boolean()),
        schema="dw",
    )

    op.create_table(
        "fato_financeiro_aps",
        sa.Column("id_fato_fin", sa.BigInteger(), primary_key=True),
        sa.Column("id_tempo", sa.Integer(), sa.ForeignKey("dw.dim_tempo.id_tempo"), nullable=False),
        sa.Column("id_municipio", sa.Integer(), sa.ForeignKey("dw.dim_municipio.id_municipio"), nullable=False),
        sa.Column("tipo_recurso", sa.String(length=50)),
        sa.Column("programa", sa.String(length=100)),
        sa.Column("valor_creditado", sa.Numeric(18, 2)),
        sa.Column("competencia_ref", sa.String(length=7)),
        sa.Column("origem_dado", sa.String(length=50)),
        schema="dw",
    )


def downgrade() -> None:
    op.drop_table("fato_financeiro_aps", schema="dw")
    op.drop_table("fato_indicador_aps", schema="dw")
    op.drop_table("fato_atendimento_aps", schema="dw")
    op.drop_table("fato_cadastro_aps", schema="dw")
    op.drop_table("dim_indicador", schema="dw")
    op.drop_table("dim_paciente", schema="dw")
    op.drop_table("dim_territorio", schema="dw")
    op.drop_table("dim_profissional", schema="dw")
    op.drop_table("dim_equipe", schema="dw")
    op.drop_table("dim_unidade_saude", schema="dw")
    op.drop_table("dim_municipio", schema="dw")
    op.drop_table("dim_tempo", schema="dw")
    op.execute("DROP SCHEMA IF EXISTS dw")

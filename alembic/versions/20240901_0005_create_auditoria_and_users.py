"""create auth and audit tables

Revision ID: 20240901_0005
Revises: 20240901_0004
Create Date: 2024-09-01 04:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20240901_0005"
down_revision = "20240901_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "app_perfil",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(length=50), nullable=False, unique=True),
        sa.Column("descricao", sa.Text()),
    )

    op.create_table(
        "app_usuario",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=False, unique=True),
        sa.Column("senha_hash", sa.String(length=255), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("perfil_id", sa.Integer(), sa.ForeignKey("app_perfil.id"), nullable=False),
        sa.Column("id_municipio", sa.Integer(), sa.ForeignKey("dw.dim_municipio.id_municipio")),
    )

    op.create_table(
        "app_auditoria_acesso",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("usuario_id", sa.Integer(), sa.ForeignKey("app_usuario.id")),
        sa.Column("perfil_nome", sa.String(length=50)),
        sa.Column("endpoint", sa.String(length=255), nullable=False),
        sa.Column("metodo_http", sa.String(length=10), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("ip_cliente", sa.String(length=45)),
        sa.Column("user_agent", sa.String(length=255)),
        sa.Column("descricao", sa.Text()),
        sa.Column("sucesso", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )


def downgrade() -> None:
    op.drop_table("app_auditoria_acesso")
    op.drop_table("app_usuario")
    op.drop_table("app_perfil")

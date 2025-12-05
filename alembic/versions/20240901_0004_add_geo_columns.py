"""add latitude/longitude to dw dimensions

Revision ID: 20240901_0004
Revises: 20240901_0003
Create Date: 2024-09-01 03:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20240901_0004"
down_revision = "20240901_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("dim_unidade_saude", sa.Column("latitude", sa.Numeric(10, 6)), schema="dw")
    op.add_column("dim_unidade_saude", sa.Column("longitude", sa.Numeric(10, 6)), schema="dw")
    op.add_column("dim_territorio", sa.Column("latitude", sa.Numeric(10, 6)), schema="dw")
    op.add_column("dim_territorio", sa.Column("longitude", sa.Numeric(10, 6)), schema="dw")


def downgrade() -> None:
    op.drop_column("dim_territorio", "longitude", schema="dw")
    op.drop_column("dim_territorio", "latitude", schema="dw")
    op.drop_column("dim_unidade_saude", "longitude", schema="dw")
    op.drop_column("dim_unidade_saude", "latitude", schema="dw")

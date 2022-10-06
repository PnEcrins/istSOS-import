"""Initial migration.

Revision ID: d70aff00e731
Revises: 
Create Date: 2022-10-05 17:30:24.783186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d70aff00e731"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "imports",
        sa.Column("id_import", sa.Integer(), nullable=False),
        sa.Column(
            "date_import", sa.DateTime(), nullable=True, server_default=sa.func.now()
        ),
        sa.Column("email", sa.Unicode(), nullable=True),
        sa.Column("id_prc", sa.Integer(), nullable=True),
        sa.Column("nb_row_total", sa.Integer(), nullable=True),
        sa.Column("nb_row_inserted", sa.Integer(), nullable=True),
        sa.Column("error_file", sa.Unicode(), nullable=True),
        sa.Column("file_name", sa.Unicode(), nullable=True),
        sa.PrimaryKeyConstraint("id_import"),
        schema="public",
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("imports", schema="public")

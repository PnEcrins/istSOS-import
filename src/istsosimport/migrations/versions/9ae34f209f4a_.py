"""empty message

Revision ID: 9ae34f209f4a
Revises: d70aff00e731
Create Date: 2022-10-06 12:33:45.596717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9ae34f209f4a"
down_revision = "d70aff00e731"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("imports", sa.Column("delimiter", sa.Unicode(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("imports", "delimiter")
    # ### end Alembic commands ###

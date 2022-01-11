"""fix grade

Revision ID: 98f20a131177
Revises: 115a58b44355
Create Date: 2022-01-11 14:51:06.755134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98f20a131177'
down_revision = '115a58b44355'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('grades', sa.Column('grade', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('grades', 'grade')
    # ### end Alembic commands ###

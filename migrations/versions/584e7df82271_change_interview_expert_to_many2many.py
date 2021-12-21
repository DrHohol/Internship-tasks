"""change interview expert to many2many

Revision ID: 584e7df82271
Revises: 6ae72853fbb9
Create Date: 2021-12-17 10:33:55.865491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '584e7df82271'
down_revision = '6ae72853fbb9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('expert_ident',
    sa.Column('expert_uname', sa.String(), nullable=True),
    sa.Column('interview_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['expert_uname'], ['user.username'], ),
    sa.ForeignKeyConstraint(['interview_id'], ['interview.id'], )
    )
    op.drop_constraint('interview_recrutier_fkey', 'interview', type_='foreignkey')
    op.drop_column('interview', 'recrutier')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('interview', sa.Column('recrutier', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.create_foreign_key('interview_recrutier_fkey', 'interview', 'user', ['recrutier'], ['username'])
    op.drop_table('expert_ident')
    # ### end Alembic commands ###

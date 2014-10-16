"""empty message

Revision ID: 5acc2b3ec29b
Revises: 3581273ba773
Create Date: 2014-10-15 23:54:03.711648

"""

# revision identifiers, used by Alembic.
revision = '5acc2b3ec29b'
down_revision = '3581273ba773'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('team', sa.Column('caseNumber', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('team', 'caseNumber')
    ### end Alembic commands ###

"""delete test column

Revision ID: 258c7c0a2724
Revises: 338903f47d74
Create Date: 2014-04-23 19:40:21.414611

"""

# revision identifiers, used by Alembic.
revision = '258c7c0a2724'
down_revision = '338903f47d74'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'test')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('test', sa.VARCHAR(length=20), nullable=True))
    ### end Alembic commands ###

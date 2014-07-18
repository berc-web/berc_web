"""empty message

Revision ID: e296bbb1b2c
Revises: 2a9761f1c3da
Create Date: 2014-07-20 15:27:26.534048

"""

# revision identifiers, used by Alembic.
revision = 'e296bbb1b2c'
down_revision = '2a9761f1c3da'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('news', sa.Column('author', sa.String(length=100), nullable=True))
    op.add_column('news', sa.Column('content', sa.String(), nullable=True))
    op.add_column('news', sa.Column('time', sa.DateTime(), nullable=True))
    op.drop_column('news', 'Content')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('news', sa.Column('Content', sa.VARCHAR(), nullable=True))
    op.drop_column('news', 'time')
    op.drop_column('news', 'content')
    op.drop_column('news', 'author')
    ### end Alembic commands ###

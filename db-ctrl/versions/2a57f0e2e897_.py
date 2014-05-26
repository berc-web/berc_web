"""empty message

Revision ID: 2a57f0e2e897
Revises: 1c5cdb0a116c
Create Date: 2014-05-20 17:48:39.801533

"""

# revision identifiers, used by Alembic.
revision = '2a57f0e2e897'
down_revision = '1c5cdb0a116c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('photo')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('photo',
    sa.Column('id', sa.INTEGER(), server_default="nextval('photo_id_seq'::regclass)", nullable=False),
    sa.Column('filename', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'photo_pkey')
    )
    ### end Alembic commands ###
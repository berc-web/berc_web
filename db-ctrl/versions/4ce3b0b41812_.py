"""empty message

Revision ID: 4ce3b0b41812
Revises: 5acc2b3ec29b
Create Date: 2014-10-18 22:46:06.208877

"""

# revision identifiers, used by Alembic.
revision = '4ce3b0b41812'
down_revision = '5acc2b3ec29b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('personal_notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=400), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'comment', sa.Column('parent_comment_id', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'comment', 'parent_comment_id')
    op.drop_table('personal_notification')
    ### end Alembic commands ###

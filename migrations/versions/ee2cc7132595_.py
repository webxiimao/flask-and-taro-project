"""empty message

Revision ID: ee2cc7132595
Revises: 87116ea7625a
Create Date: 2018-10-30 09:43:11.629927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee2cc7132595'
down_revision = '87116ea7625a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('isDelete', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'isDelete')
    # ### end Alembic commands ###

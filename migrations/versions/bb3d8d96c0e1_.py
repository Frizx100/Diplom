"""empty message

Revision ID: bb3d8d96c0e1
Revises: 
Create Date: 2023-04-20 15:51:22.709290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb3d8d96c0e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('series',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('anime', sa.Integer(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('path', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['anime'], ['anime.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('series')
    # ### end Alembic commands ###

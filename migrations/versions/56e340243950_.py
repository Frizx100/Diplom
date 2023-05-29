"""empty message

Revision ID: 56e340243950
Revises: 
Create Date: 2023-05-29 15:30:38.934491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56e340243950'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('anime_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_anime_status'))
    )
    op.create_table('genre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_genre'))
    )
    op.create_table('rate_age',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rate', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_rate_age'))
    )
    op.create_table('type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_type'))
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('reg_date', sa.Date(), nullable=True),
    sa.Column('about', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('username', name=op.f('uq_user_username'))
    )
    op.create_table('watch_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_watch_status'))
    )
    op.create_table('anime',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('altName', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('seriesCount', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('reliese_type', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('_genre', sa.String(), nullable=True),
    sa.Column('fullDescription', sa.String(), nullable=False),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('ageRate', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ageRate'], ['rate_age.id'], name=op.f('fk_anime_ageRate_rate_age')),
    sa.ForeignKeyConstraint(['reliese_type'], ['type.id'], name=op.f('fk_anime_reliese_type_type')),
    sa.ForeignKeyConstraint(['status'], ['anime_status.id'], name=op.f('fk_anime_status_anime_status')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_anime'))
    )
    op.create_table('check_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('anime', sa.Integer(), nullable=True),
    sa.Column('lastSeries', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['anime'], ['anime.id'], name=op.f('fk_check_list_anime_anime')),
    sa.ForeignKeyConstraint(['status'], ['watch_status.id'], name=op.f('fk_check_list_status_watch_status')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_check_list_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_check_list'))
    )
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('grade', sa.Integer(), nullable=True),
    sa.Column('anime', sa.Integer(), nullable=True),
    sa.Column('author', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['anime'], ['anime.id'], name=op.f('fk_review_anime_anime')),
    sa.ForeignKeyConstraint(['author'], ['user.id'], name=op.f('fk_review_author_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_review'))
    )
    op.create_table('series',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('anime', sa.Integer(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('path', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['anime'], ['anime.id'], name=op.f('fk_series_anime_anime')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_series'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('series')
    op.drop_table('review')
    op.drop_table('check_list')
    op.drop_table('anime')
    op.drop_table('watch_status')
    op.drop_table('user')
    op.drop_table('type')
    op.drop_table('rate_age')
    op.drop_table('genre')
    op.drop_table('anime_status')
    # ### end Alembic commands ###

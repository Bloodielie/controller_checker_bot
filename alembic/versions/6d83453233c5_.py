"""empty message

Revision ID: 6d83453233c5
Revises: 
Create Date: 2020-08-13 20:22:41.146298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d83453233c5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number_of_posts', sa.Integer(), nullable=True),
    sa.Column('city', sa.String(length=20), nullable=True),
    sa.Column('representation', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('telegram_id', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('time_of_last_receipt', sa.DateTime(), nullable=True),
    sa.Column('settings_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['settings_id'], ['settings.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('busstop',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message_text', sa.Text(), nullable=True),
    sa.Column('city', sa.String(length=20), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('busstop')
    op.drop_table('users')
    op.drop_table('settings')
    # ### end Alembic commands ###

"""add post model

Revision ID: 8d733c035279
Revises: 4696c0b2c865
Create Date: 2023-07-09 00:39:19.050403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d733c035279'
down_revision = '4696c0b2c865'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_description'), 'post', ['description'], unique=False)
    op.create_index(op.f('ix_post_id'), 'post', ['id'], unique=False)
    op.create_index(op.f('ix_post_title'), 'post', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_title'), table_name='post')
    op.drop_index(op.f('ix_post_id'), table_name='post')
    op.drop_index(op.f('ix_post_description'), table_name='post')
    op.drop_table('post')
    # ### end Alembic commands ###
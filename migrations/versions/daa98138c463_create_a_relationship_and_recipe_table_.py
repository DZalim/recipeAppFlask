"""Create a relationship and recipe table with other helper tables

Revision ID: daa98138c463
Revises: 321b4dec3349
Create Date: 2024-10-05 18:39:27.085762

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'daa98138c463'
down_revision = '321b4dec3349'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_name', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('category_name')
    )
    op.create_table('recipes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_name', sa.String(length=255), nullable=False),
    sa.Column('difficulty_level', sa.Enum('easy', 'medium', 'hard', name='recipedifficultylevel'), server_default='easy', nullable=False),
    sa.Column('portions', sa.Integer(), nullable=False),
    sa.Column('preparing_time_in_minutes', sa.Integer(), nullable=False),
    sa.Column('cooking_time_in_minutes', sa.Integer(), nullable=False),
    sa.Column('ingredients', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('recipe_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipes')
    op.drop_table('categories')
    # ### end Alembic commands ###

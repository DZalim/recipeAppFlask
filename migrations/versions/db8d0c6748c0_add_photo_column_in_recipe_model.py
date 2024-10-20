"""Add photo column in recipe model

Revision ID: db8d0c6748c0
Revises: daa98138c463
Create Date: 2024-10-13 16:22:40.097512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db8d0c6748c0'
down_revision = 'daa98138c463'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('recipe_photo_url', sa.String(length=255), server_default='No photo'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.drop_column('recipe_photo_url')

    # ### end Alembic commands ###

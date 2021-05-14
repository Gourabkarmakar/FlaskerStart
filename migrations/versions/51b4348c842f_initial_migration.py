"""Initial Migration

Revision ID: 51b4348c842f
Revises: 
Create Date: 2021-05-14 15:11:21.187408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51b4348c842f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('favorite_color', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'favorite_color')
    # ### end Alembic commands ###

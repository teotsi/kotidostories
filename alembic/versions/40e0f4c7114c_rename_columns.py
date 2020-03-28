"""rename columns

Revision ID: 40e0f4c7114c
Revises: 249573d41088
Create Date: 2020-03-28 05:36:08.455077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40e0f4c7114c'
down_revision = '249573d41088'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('post') as bop:
        bop.alter_column('post_img', new_column_name='img')
    with op.batch_alter_table('user') as bop:
        bop.alter_column('user_img', new_column_name='img')


def downgrade():
    pass

"""Add post img

Revision ID: 80d57accd844
Revises: 45ca9989d638
Create Date: 2020-03-28 04:20:50.289404

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import Column, String

# revision identifiers, used by Alembic.


revision = '80d57accd844'
down_revision = '45ca9989d638'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('post', Column('post_img', String(), server_default='pictures/post/default.png'))


def downgrade():
    drop_column_sqlite('post', ['post_img'])


def drop_column_sqlite(tablename, columns):
    """ column dropping functionality for SQLite
        Many thanks to @klugjohannes
    """

    # we need copy to make a deep copy of the column attributes
    from copy import copy

    # get the db engine and reflect database tables
    engine = op.get_bind()
    meta = sa.MetaData(bind=engine)
    meta.reflect()

    # create a select statement from the old table
    old_table = meta.tables[tablename]
    select = sa.sql.select([c for c in old_table.c if c.name not in columns])

    # get remaining columns without table attribute attached
    remaining_columns = [copy(c) for c in old_table.columns
                         if c.name not in columns]
    for column in remaining_columns:
        column.table = None

    # create a temporary new table
    new_tablename = '{0}_new'.format(tablename)
    op.create_table(new_tablename, *remaining_columns)
    meta.reflect()
    new_table = meta.tables[new_tablename]

    # copy data from old table
    insert = sa.sql.insert(new_table).from_select(
        [c.name for c in remaining_columns], select)
    engine.execute(insert)

    # drop the old table and rename the new table to take the old tables
    # position
    op.drop_table(tablename)
    op.rename_table(new_tablename, tablename)

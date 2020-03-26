"""add post type

Revision ID: 45ca9989d638
Revises: 
Create Date: 2020-03-27 00:32:44.405742

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import Column, Enum

# revision identifiers, used by Alembic.

revision = '45ca9989d638'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('post') as batch_op:
        op.add_column('post', Column('category', Enum(), nullable=False, server_default='story'))
        batch_op.alter_column('category', 'post', server_default=None)


def downgrade():
    drop_column_sqlite('post', ['category'])


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

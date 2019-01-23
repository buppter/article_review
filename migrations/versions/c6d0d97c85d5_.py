"""empty message

Revision ID: c6d0d97c85d5
Revises: 2218c6305ae0
Create Date: 2019-01-23 14:54:08.391771

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c6d0d97c85d5'
down_revision = '2218c6305ae0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('new_submission', sa.Column('associate_editor_id', sa.Integer(), nullable=True))
    op.drop_constraint('new_submission_ibfk_4', 'new_submission', type_='foreignkey')
    op.create_foreign_key(None, 'new_submission', 'users', ['associate_editor_id'], ['id'])
    op.drop_column('new_submission', 'associate_editor')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('new_submission', sa.Column('associate_editor', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'new_submission', type_='foreignkey')
    op.create_foreign_key('new_submission_ibfk_4', 'new_submission', 'users', ['associate_editor'], ['id'])
    op.drop_column('new_submission', 'associate_editor_id')
    # ### end Alembic commands ###
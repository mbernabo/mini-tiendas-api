"""Mejoro la col fecha de la tabla Auditoria

Revision ID: 7d1e2475491f
Revises: 9c1db37774a1
Create Date: 2024-05-13 20:11:24.444376

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7d1e2475491f'
down_revision = '9c1db37774a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('auditoria', schema=None) as batch_op:
        batch_op.alter_column('fecha',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('auditoria', schema=None) as batch_op:
        batch_op.alter_column('fecha',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)

    # ### end Alembic commands ###

"""empty message

Revision ID: 39edb53c8026
Revises: c623bbf097ac
Create Date: 2024-05-01 19:24:08.648078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39edb53c8026'
down_revision = 'c623bbf097ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('auditoria', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tabla_asociada', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('registro_asociado', sa.Integer(), nullable=True))
        batch_op.drop_column('tienda_asociada_id')
        batch_op.drop_column('item_asociado_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('auditoria', schema=None) as batch_op:
        batch_op.add_column(sa.Column('item_asociado_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('tienda_asociada_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_column('registro_asociado')
        batch_op.drop_column('tabla_asociada')

    # ### end Alembic commands ###
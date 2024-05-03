"""empty message

Revision ID: 645b1ffdb876
Revises: 39edb53c8026
Create Date: 2024-05-01 19:35:52.717748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '645b1ffdb876'
down_revision = '39edb53c8026'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('auditoria', schema=None) as batch_op:
        batch_op.alter_column('tabla_asociada',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('auditoria', schema=None) as batch_op:
        batch_op.alter_column('tabla_asociada',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###
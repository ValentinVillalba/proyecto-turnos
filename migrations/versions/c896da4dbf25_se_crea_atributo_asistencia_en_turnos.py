"""se crea atributo asistencia en turnos

Revision ID: c896da4dbf25
Revises: a17df46d0f03
Create Date: 2024-06-25 14:43:12.902199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c896da4dbf25'
down_revision = 'a17df46d0f03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('turnos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('asistencia', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('turnos', schema=None) as batch_op:
        batch_op.drop_column('asistencia')

    # ### end Alembic commands ###

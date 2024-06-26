"""Se modifica la tabla usuarios

Revision ID: 6aed5a947322
Revises: 4469d089f480
Create Date: 2024-06-17 13:53:56.456170

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6aed5a947322'
down_revision = '4469d089f480'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=20), nullable=False))
        batch_op.drop_column('contraseña')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contraseña', mysql.VARCHAR(length=8), nullable=False))
        batch_op.drop_column('password')

    # ### end Alembic commands ###

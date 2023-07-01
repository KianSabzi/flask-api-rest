"""empty message

Revision ID: e7e7f4173fbe
Revises: 717cdddc2fa4
Create Date: 2023-07-02 00:47:30.307986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7e7f4173fbe'
down_revision = '717cdddc2fa4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=80), nullable=True))
        batch_op.add_column(sa.Column('phone_number', sa.String(length=30), nullable=False))
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=250),
               nullable=True)
        batch_op.create_unique_constraint(None, ['phone_number'])
        batch_op.create_unique_constraint(None, ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
        batch_op.drop_column('phone_number')
        batch_op.drop_column('email')

    # ### end Alembic commands ###

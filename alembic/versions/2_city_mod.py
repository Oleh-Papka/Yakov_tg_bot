"""city_mod

Revision ID: 2
Revises: 1
Create Date: 2022-08-07 14:13:34.861104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2'
down_revision = '1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.alter_column('currency_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('city', schema=None) as batch_op:
        batch_op.add_column(sa.Column('url', sa.TEXT(), nullable=False))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('city', schema=None) as batch_op:
        batch_op.drop_column('url')

    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.alter_column('currency_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
"""initial_table_creation

Revision ID: 0001
Revises:
Create Date: 2023-03-05 18:52:51.348523

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('city',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('owm_id', sa.INTEGER(), nullable=False),
                    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
                    sa.Column('local_name', sa.VARCHAR(length=50), nullable=True),
                    sa.Column('lat', sa.REAL(), nullable=True),
                    sa.Column('lon', sa.REAL(), nullable=True),
                    sa.Column('sinoptik_url', sa.TEXT(), nullable=True),
                    sa.Column('timezone_offset', sa.INTEGER(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('crypto_currency',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('name', sa.VARCHAR(length=20), nullable=False),
                    sa.Column('abbr', sa.VARCHAR(length=10), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('currency',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=5), nullable=False),
                    sa.Column('symbol', sa.VARCHAR(length=5), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('user',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
                    sa.Column('first_name', sa.VARCHAR(length=64), nullable=False),
                    sa.Column('last_name', sa.VARCHAR(length=64), nullable=True),
                    sa.Column('joined', sa.TIMESTAMP(), nullable=False),
                    sa.Column('language_code', sa.VARCHAR(length=2), nullable=False),
                    sa.Column('timezone_offset', sa.INTEGER(), nullable=True),
                    sa.Column('active', sa.BOOLEAN(), nullable=False),
                    sa.Column('city_id', sa.INTEGER(), nullable=True),
                    sa.ForeignKeyConstraint(['city_id'], ['city.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('crypto_currency_watchlist',
                    sa.Column('user_id', sa.INTEGER(), nullable=False),
                    sa.Column('crypto_currency_id', sa.INTEGER(), nullable=False),
                    sa.ForeignKeyConstraint(['crypto_currency_id'], ['crypto_currency.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('user_id', 'crypto_currency_id')
                    )
    op.create_table('currency_watchlist',
                    sa.Column('user_id', sa.INTEGER(), nullable=False),
                    sa.Column('currency_id', sa.INTEGER(), nullable=False),
                    sa.ForeignKeyConstraint(['currency_id'], ['currency.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('user_id', 'currency_id')
                    )
    op.create_table('feedback',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('user_id', sa.INTEGER(), nullable=False),
                    sa.Column('msg_id', sa.INTEGER(), nullable=False),
                    sa.Column('msg_text', sa.TEXT(), nullable=False),
                    sa.Column('read_flag', sa.BOOLEAN(), nullable=False),
                    sa.Column('timestamp', postgresql.TIMESTAMP(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feedback')
    op.drop_table('currency_watchlist')
    op.drop_table('crypto_currency_watchlist')
    op.drop_table('user')
    op.drop_table('currency')
    op.drop_table('crypto_currency')
    op.drop_table('city')
    # ### end Alembic commands ###

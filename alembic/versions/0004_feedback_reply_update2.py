"""Feedback reply update2

Revision ID: 0004
Revises: 0003
Create Date: 2023-10-12 21:07:32.139457

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feedback_reply',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('feedback_id', sa.INTEGER(), nullable=False),
    sa.Column('msg_id', sa.INTEGER(), nullable=False),
    sa.Column('msg_text', sa.TEXT(), nullable=False),
    sa.Column('timestamp', postgresql.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['feedback_id'], ['feedback.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('feedback', sa.Column('pinned_msg_id', sa.INTEGER(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('feedback', 'pinned_msg_id')
    op.drop_table('feedback_reply')
    # ### end Alembic commands ###

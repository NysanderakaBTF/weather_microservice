"""init

Revision ID: 1b1b42e151f0
Revises: 
Create Date: 2023-10-18 17:53:37.938969

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b1b42e151f0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cities',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('weather',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('city_id', sa.BigInteger(), nullable=True),
    sa.Column('temperature', sa.Float(), nullable=False),
    sa.Column('pressure', sa.Float(), nullable=False),
    sa.Column('wind_speed', sa.Float(), nullable=False),
    sa.Column('timestamp', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('weather')
    op.drop_table('cities')
    # ### end Alembic commands ###

"""empty message

Revision ID: a0834fe77f0a
Revises: b4addfc13a5f
Create Date: 2024-10-11 22:28:17.064748

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a0834fe77f0a'
down_revision: Union[str, None] = 'b4addfc13a5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('test_laboratories', 'test_date_finish',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.String(),
               existing_nullable=True,
               existing_server_default=sa.text("timezone('utc'::text, now())"))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('test_laboratories', 'test_date_finish',
               existing_type=sa.String(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True,
               existing_server_default=sa.text("timezone('utc'::text, now())"))
    # ### end Alembic commands ###

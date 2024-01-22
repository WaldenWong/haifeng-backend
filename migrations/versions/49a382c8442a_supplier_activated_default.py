"""supplier_activated_default

Revision ID: 49a382c8442a
Revises: 7afa56791c28
Create Date: 2024-01-22 23:48:33.256011

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "49a382c8442a"
down_revision: Union[str, None] = "7afa56791c28"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "supplier", sa.Column("activated", sa.Boolean(), server_default=sa.text("true"), nullable=True, comment="是否启用")
    )
    op.drop_index("ix_supplier_disable", table_name="supplier")
    op.create_index(op.f("ix_supplier_activated"), "supplier", ["activated"], unique=False)
    op.drop_column("supplier", "disable")
    op.drop_index("ix_user_disable", table_name="user")
    op.drop_column("user", "disable")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user",
        sa.Column(
            "disable", sa.BOOLEAN(), server_default=sa.text("true"), autoincrement=False, nullable=True, comment="是否禁用"
        ),
    )
    op.create_index("ix_user_disable", "user", ["disable"], unique=False)
    op.add_column("supplier", sa.Column("disable", sa.BOOLEAN(), autoincrement=False, nullable=True, comment="是否禁用"))
    op.drop_index(op.f("ix_supplier_activated"), table_name="supplier")
    op.create_index("ix_supplier_disable", "supplier", ["disable"], unique=False)
    op.drop_column("supplier", "activated")
    # ### end Alembic commands ###
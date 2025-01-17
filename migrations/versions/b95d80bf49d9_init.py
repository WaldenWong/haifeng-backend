"""init

Revision ID: b95d80bf49d9
Revises:
Create Date: 2023-05-24 00:58:31.161713

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "b95d80bf49d9"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "login_log",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("ip", sa.String(length=128), nullable=False),
        sa.Column("port", sa.Integer(), nullable=False),
        sa.Column("country", sa.String(length=64), nullable=True),
        sa.Column("province", sa.String(length=64), nullable=True),
        sa.Column("city", sa.String(length=64), nullable=True),
        sa.Column("is_pc", sa.Boolean(), nullable=True),
        sa.Column("device", sa.String(length=128), nullable=True),
        sa.Column("os", sa.String(length=128), nullable=False),
        sa.Column("browser", sa.String(length=128), nullable=False),
        sa.Column("ua", sa.String(length=512), nullable=False),
        sa.Column("headers", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_login_log_city"), "login_log", ["city"], unique=False)
    op.create_index(op.f("ix_login_log_created_on"), "login_log", ["created_on"], unique=False)
    op.create_index(op.f("ix_login_log_ip"), "login_log", ["ip"], unique=False)
    op.create_index(op.f("ix_login_log_updated_on"), "login_log", ["updated_on"], unique=False)
    op.create_index(op.f("ix_login_log_user_id"), "login_log", ["user_id"], unique=False)
    op.create_table(
        "role_group",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.Column("shows", postgresql.ARRAY(sa.String(length=32)), nullable=False),
        sa.Column("roles", postgresql.ARRAY(sa.String(length=32)), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("config", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_role_group_created_on"), "role_group", ["created_on"], unique=False)
    op.create_index(op.f("ix_role_group_name"), "role_group", ["name"], unique=True)
    op.create_index(op.f("ix_role_group_updated_on"), "role_group", ["updated_on"], unique=False)
    op.create_index(op.f("ix_role_group_user_id"), "role_group", ["user_id"], unique=False)
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("username", sa.String(length=32), nullable=False),
        sa.Column("password", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=32), nullable=True),
        sa.Column("phone", sa.String(length=11), nullable=True),
        sa.Column("realname", sa.String(length=11), nullable=True),
        sa.Column("province", sa.String(length=32), nullable=True),
        sa.Column("city", sa.String(length=32), nullable=True),
        sa.Column("district", sa.String(length=32), nullable=True),
        sa.Column("avatar", sa.String(length=256), nullable=True),
        sa.Column("api_key", sa.String(length=256), nullable=True),
        sa.Column("expired_at", sa.DateTime(), nullable=True),
        sa.Column("stopped_on", sa.DateTime(), nullable=True),
        sa.Column("activated", sa.Boolean(), server_default=sa.text("true"), nullable=True),
        sa.Column("group", sa.BigInteger(), nullable=False),
        sa.Column("creator", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("api_key"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("phone"),
        sa.UniqueConstraint("username", name="uc_user_username"),
    )
    op.create_index(op.f("ix_user_activated"), "user", ["activated"], unique=False)
    op.create_index(op.f("ix_user_city"), "user", ["city"], unique=False)
    op.create_index(op.f("ix_user_created_on"), "user", ["created_on"], unique=False)
    op.create_index(op.f("ix_user_creator"), "user", ["creator"], unique=False)
    op.create_index(op.f("ix_user_district"), "user", ["district"], unique=False)
    op.create_index(op.f("ix_user_province"), "user", ["province"], unique=False)
    op.create_index(op.f("ix_user_updated_on"), "user", ["updated_on"], unique=False)
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=False)
    op.create_table(
        "user_group",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.Column("show", postgresql.ARRAY(sa.String(length=32)), nullable=False),
        sa.Column("role_group", sa.BigInteger(), nullable=False),
        sa.Column("creator", sa.BigInteger(), nullable=False),
        sa.Column("province", sa.String(length=64), nullable=True),
        sa.Column("city", sa.String(length=64), nullable=True),
        sa.Column("district", sa.String(length=64), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_group_city"), "user_group", ["city"], unique=False)
    op.create_index(op.f("ix_user_group_created_on"), "user_group", ["created_on"], unique=False)
    op.create_index(op.f("ix_user_group_creator"), "user_group", ["creator"], unique=False)
    op.create_index(op.f("ix_user_group_district"), "user_group", ["district"], unique=False)
    op.create_index(op.f("ix_user_group_name"), "user_group", ["name"], unique=True)
    op.create_index(op.f("ix_user_group_province"), "user_group", ["province"], unique=False)
    op.create_index(op.f("ix_user_group_role_group"), "user_group", ["role_group"], unique=False)
    op.create_index(op.f("ix_user_group_updated_on"), "user_group", ["updated_on"], unique=False)
    op.create_table(
        "user_role",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_on", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("role", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("user_group_id", sa.BigInteger(), nullable=True),
        sa.Column("show", sa.String(length=64), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_role_created_on"), "user_role", ["created_on"], unique=False)
    op.create_index(op.f("ix_user_role_role"), "user_role", ["role"], unique=False)
    op.create_index(op.f("ix_user_role_updated_on"), "user_role", ["updated_on"], unique=False)
    op.create_index(op.f("ix_user_role_user_group_id"), "user_role", ["user_group_id"], unique=False)
    op.create_index(op.f("ix_user_role_user_id"), "user_role", ["user_id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_role_user_id"), table_name="user_role")
    op.drop_index(op.f("ix_user_role_user_group_id"), table_name="user_role")
    op.drop_index(op.f("ix_user_role_updated_on"), table_name="user_role")
    op.drop_index(op.f("ix_user_role_role"), table_name="user_role")
    op.drop_index(op.f("ix_user_role_created_on"), table_name="user_role")
    op.drop_table("user_role")
    op.drop_index(op.f("ix_user_group_updated_on"), table_name="user_group")
    op.drop_index(op.f("ix_user_group_role_group"), table_name="user_group")
    op.drop_index(op.f("ix_user_group_province"), table_name="user_group")
    op.drop_index(op.f("ix_user_group_name"), table_name="user_group")
    op.drop_index(op.f("ix_user_group_district"), table_name="user_group")
    op.drop_index(op.f("ix_user_group_creator"), table_name="user_group")
    op.drop_index(op.f("ix_user_group_created_on"), table_name="user_group")
    op.drop_index(op.f("ix_user_group_city"), table_name="user_group")
    op.drop_table("user_group")
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_index(op.f("ix_user_updated_on"), table_name="user")
    op.drop_index(op.f("ix_user_province"), table_name="user")
    op.drop_index(op.f("ix_user_district"), table_name="user")
    op.drop_index(op.f("ix_user_creator"), table_name="user")
    op.drop_index(op.f("ix_user_created_on"), table_name="user")
    op.drop_index(op.f("ix_user_city"), table_name="user")
    op.drop_index(op.f("ix_user_activated"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_role_group_user_id"), table_name="role_group")
    op.drop_index(op.f("ix_role_group_updated_on"), table_name="role_group")
    op.drop_index(op.f("ix_role_group_name"), table_name="role_group")
    op.drop_index(op.f("ix_role_group_created_on"), table_name="role_group")
    op.drop_table("role_group")
    op.drop_index(op.f("ix_login_log_user_id"), table_name="login_log")
    op.drop_index(op.f("ix_login_log_updated_on"), table_name="login_log")
    op.drop_index(op.f("ix_login_log_ip"), table_name="login_log")
    op.drop_index(op.f("ix_login_log_created_on"), table_name="login_log")
    op.drop_index(op.f("ix_login_log_city"), table_name="login_log")
    op.drop_table("login_log")
    # ### end Alembic commands ###

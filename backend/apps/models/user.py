#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from sqlalchemy import text

from backend.apps.models import Base, db
from backend.apps.settings import settings


def default_expired_at() -> datetime:
    return datetime.now() + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)


class User(Base):
    __tablename__ = "user"
    __table_args__ = {
        # 'mysql_engine': 'MyISAM',
        "comment": "用户信息"
    }

    username = db.Column(db.String(32), index=True, comment="用户名")
    password = db.Column(db.String(100), comment="密码")
    phone = db.Column(db.String(11), unique=True, nullable=True, comment="电话")
    real_name = db.Column(db.String(11), nullable=True, comment="真实姓名")
    avatar = db.Column(db.String(256), nullable=True, comment="头像")  # 头像
    expired_at = db.Column(db.DateTime(), default=default_expired_at, comment="用户Jwt到期时间")
    stopped_on = db.Column(db.DateTime(), nullable=True, comment="账号过期时间")
    activated = db.Column(db.Boolean(), index=True, server_default=text("true"), comment="是否启用")
    creator = db.Column(db.BigInteger(), index=True, nullable=True, comment="创建人")

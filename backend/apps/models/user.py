#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from sqlalchemy import text

from backend.apps.models import Base, BaseMeta, orm
from backend.apps.settings import settings


def default_expired_at() -> datetime:
    return datetime.now() + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)


class User(Base):
    class Meta(BaseMeta):
        tablename = "user"
        constraints = [orm.UniqueColumns("username")]

    username = orm.String(max_length=32, index=True)
    password = orm.String(max_length=100)
    phone = orm.String(max_length=11, unique=True, nullable=True)
    real_name = orm.String(max_length=11, nullable=True)
    avatar = orm.String(max_length=256, nullable=True)  # 头像
    expired_at = orm.DateTime(default=default_expired_at)  # 登录时到期时间
    stopped_on = orm.DateTime(nullable=True)  # 账户到期时间
    activated = orm.Boolean(index=True, server_default=text("true"))

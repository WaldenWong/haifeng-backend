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
    email = orm.String(max_length=32, unique=True, nullable=True)
    phone = orm.String(max_length=11, unique=True, nullable=True)
    realname = orm.String(max_length=11, nullable=True)
    province = orm.String(max_length=32, index=True, nullable=True)
    city = orm.String(max_length=32, index=True, nullable=True)
    district = orm.String(max_length=32, index=True, nullable=True)
    avatar = orm.String(max_length=256, nullable=True)  # 头像
    api_key = orm.String(max_length=256, unique=True, nullable=True)
    expired_at = orm.DateTime(default=default_expired_at)
    stopped_on = orm.DateTime(nullable=True)
    activated = orm.Boolean(index=True, server_default=text("true"))
    group = orm.BigInteger()
    creator = orm.BigInteger(index=True, nullable=True)

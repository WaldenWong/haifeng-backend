#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend.apps.models import Base, BaseMeta, orm


class LoginLog(Base):
    class Meta(BaseMeta):
        tablename = "login_log"

    user_id = orm.BigInteger(index=True)
    ip = orm.String(max_length=128, index=True)
    port = orm.Integer()
    country = orm.String(max_length=64, nullable=True)
    province = orm.String(max_length=64, nullable=True)
    city = orm.String(max_length=64, index=True, nullable=True)
    is_pc = orm.Boolean(nullable=True)
    device = orm.String(max_length=128, nullable=True)
    os = orm.String(max_length=128)
    browser = orm.String(max_length=128)
    ua = orm.String(max_length=512)
    headers = orm.JSON()

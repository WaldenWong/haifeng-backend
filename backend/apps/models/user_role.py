#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend.apps.models import Base, BaseMeta, orm


class UserRole(Base):
    class Meta(BaseMeta):
        tablename = "user_role"

    role = orm.String(max_length=64, index=True)
    user_id = orm.BigInteger(index=True)
    user_group_id = orm.BigInteger(nullable=True, index=True)
    show = orm.String(max_length=64, nullable=True)

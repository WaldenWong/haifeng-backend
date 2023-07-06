#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend.apps.models import Base, BaseMeta, orm, orm_ext, sa


class UserGroup(Base):
    class Meta(BaseMeta):
        tablename = "user_group"

    name: str = orm.String(max_length=32, unique=True, index=True)
    show: list = orm_ext.ARRAY(item_type=sa.String(32))
    role_group: int = orm.BigInteger(index=True)
    creator: int = orm.BigInteger(index=True)
    province: str = orm.String(max_length=64, nullable=True, index=True)
    city: str = orm.String(max_length=64, nullable=True, index=True)
    district: str = orm.String(max_length=64, nullable=True, index=True)

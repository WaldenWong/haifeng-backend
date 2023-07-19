#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.apps.models import Base, BaseMeta, orm


class Business(Base):
    # 销售商家
    class Meta(BaseMeta):
        tablename = "business"

    name = orm.String(max_length=32, unique=True, index=True)
    address = orm.String(max_length=128, index=True)  # 地址
    phone = orm.String(max_length=11, unique=True, index=True)
    manager = orm.String(max_length=32, index=True)  # 经营者名
    landline = orm.String(max_length=32, unique=True, index=True)  # 座机
    scale = orm.Integer(nullable=True, index=True)  # 规模

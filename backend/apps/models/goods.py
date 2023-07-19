#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.apps.models import Base, BaseMeta, orm


class Goods(Base):
    class Meta(BaseMeta):
        tablename = "goods"

    name = orm.String(max_length=32, unique=True, index=True)  # 商品名
    identifier = orm.String(max_length=32, nullable=True, index=True)  # 编号
    type = orm.String(max_length=32, nullable=True, index=True)  # 种类
    purchase_price = orm.Float()  # 进价
    selling_price = orm.Float()  # 售价
    inventory = orm.Integer(default=0, index=True)  # 库存
    sales_volume = orm.Integer(default=0, index=True)  # 销量
    purchase_at = orm.DateTime(index=True)  # 入库时间
    supplier = orm.Integer(index=True)  # 供应商id

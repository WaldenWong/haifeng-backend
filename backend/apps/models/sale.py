#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.apps.models import Base, BaseMeta, orm


class Sale(Base):
    # 销售表
    class Meta(BaseMeta):
        tablename = "sale"

    goods_id = orm.Integer(index=True)  # 商品id
    business = orm.Integer(index=True)  # 销售商家
    sold_at = orm.DateTime(nullable=True)  # 售出时间
    quantity = orm.Integer(default=0)  # 数量
    unit_price = orm.Float(default=0.0)  # 单价

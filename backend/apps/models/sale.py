#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.apps.models import Base, db


# 销售表
class Sale(Base):
    __tablename__ = "sale"

    goods_id = db.Column(db.Integer(), index=True)  # 商品id
    business = db.Column(db.Integer(), index=True)  # 销售商家
    sold_at = db.Column(db.DateTime(), nullable=True)  # 售出时间
    quantity = db.Column(db.Integer(), default=0)  # 数量
    unit_price = db.Column(db.Float(), default=0.0)  # 单价

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.apps.models import Base, db


class Sale(Base):
    __tablename__ = "sale"
    __table_args__ = {"comment": "销售记录"}

    goods_id = db.Column(db.Integer(), index=True)  # 商品id
    business = db.Column(db.Integer(), index=True)  # 销售商家
    sold_at = db.Column(db.DateTime(), nullable=True)  # 售出时间
    sales = db.Column(db.Integer(), default=0)  # 销量
    unit_price = db.Column(db.Float(), default=0.0)  # 单价

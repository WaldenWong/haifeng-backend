#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from backend.apps.models import Base, db


class Goods(Base):
    __tablename__ = "goods"

    name = db.Column(db.String(), unique=True, index=True)  # 商品名
    identifier = db.Column(db.String(32), nullable=True, index=True)  # 编号
    type = db.Column(db.String(32), nullable=True, index=True)  # 种类
    purchase_price = db.Column(db.Float())  # 进价
    selling_price = db.Column(db.Float())  # 售价
    inventory = db.Column(db.Integer(), default=0, index=True)  # 库存
    sales_volume = db.Column(db.Integer(), default=0, index=True)  # 销量
    purchase_at = db.Column(db.DateTime(), index=True, default=datetime.now)  # 入库时间
    supplier = db.Column(db.Integer(), index=True)  # 供应商id

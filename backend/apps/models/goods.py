#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from backend.apps.models import Base, db


class Goods(Base):
    __tablename__ = "goods"
    __table_args__ = {"comment": "商品信息"}

    name = db.Column(db.String(), unique=True, index=True, comment="商品名")
    identifier = db.Column(db.String(32), nullable=True, index=True, comment="编号")
    type = db.Column(db.String(32), nullable=True, index=True, comment="种类")
    purchase_price = db.Column(db.Float(), comment="进价")
    selling_price = db.Column(db.Float(), comment="建议售价")
    inventory = db.Column(db.Integer(), default=0, index=True, comment="库存")
    sales = db.Column(db.Integer(), default=0, comment="销量")
    month_sales = db.Column(db.Integer(), default=0, comment="月销量，为0时使用真实数据修改(最近30天该商品销量总和)")
    purchase_at = db.Column(db.DateTime(), index=True, default=datetime.now, comment="入库时间")
    supplier = db.Column(db.Integer(), index=True, comment="供应商ID")
    warranty = db.Column(db.Integer(), default=0, comment="保质期")
    notes = db.Column(db.Text(), comment="备注")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend.apps.models import Base, db


class Goods(Base):
    __tablename__ = "goods"
    __table_args__ = {"comment": "商品信息"}

    name = db.Column(db.String(), nullable=False, unique=True, index=True, comment="商品名")
    image = db.Column(db.String(256), comment="商品图片")
    identifier = db.Column(db.String(32), index=True, comment="编号")
    type = db.Column(db.String(32), nullable=True, index=True, comment="种类")
    purchase_price = db.Column(db.Float(), comment="进价")
    selling_price = db.Column(db.Float(), comment="建议售价")
    inventory = db.Column(db.Integer(), default=0, index=True, comment="库存")
    sales = db.Column(db.Integer(), default=0, comment="销量")
    month_sales = db.Column(db.Integer(), default=0, comment="月销量，为0时使用真实数据修改(最近30天该商品销量总和)")
    supplier = db.Column(db.Integer(), index=True, comment="供应商ID")
    warranty = db.Column(db.Integer(), default=0, comment="保质期")
    notes = db.Column(db.Text(), comment="备注")
    last_purchase_at = db.Column(db.DateTime(), nullable=False, index=True, comment="最近一次入库时间")

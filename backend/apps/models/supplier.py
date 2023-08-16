#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend.apps.models import Base, db


class Supplier(Base):
    __tablename__ = "supplier"
    __table_args__ = {"comment": "供应商信息"}

    name = db.Column(db.String(32), unique=True, index=True, comment="商家名")
    address = db.Column(db.String(128), index=True, comment="地址")
    phone = db.Column(db.String(11), unique=True, index=True, comment="电话，不能与备用电话重复")
    alternative_phone = db.Column(db.String(11), unique=True, index=True, comment="备用电话，不能与电话重复")
    manager = db.Column(db.String(32), index=True, comment="经营者名")
    landline = db.Column(db.String(32), unique=True, index=True, comment="座机")

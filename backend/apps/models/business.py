#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.apps.models import Base, db


# 销售商家
class Business(Base):
    __tablename__ = "business"

    name = db.Column(db.String(32), unique=True, index=True)
    address = db.Column(db.String(128), index=True)  # 地址
    phone = db.Column(db.String(11), unique=True, index=True)
    manager = db.Column(db.String(32), index=True)  # 经营者名
    landline = db.Column(db.String(32), unique=True, index=True)  # 座机
    scale = db.Column(db.Integer(), nullable=True, index=True)  # 规模

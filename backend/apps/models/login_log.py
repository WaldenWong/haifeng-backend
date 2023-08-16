#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend.apps.models import Base, db


class LoginLog(Base):
    __tablename__ = "login_log"
    __table_args__ = {"comment": "登录日志"}

    user_id = db.Column(db.BigInteger(), index=True, comment="用户ID")
    ip = db.Column(db.String(128), index=True, comment="IP")
    port = db.Column(db.Integer(), comment="端口")
    country = db.Column(db.String(64), nullable=True, comment="国")
    province = db.Column(db.String(64), nullable=True, comment="省")
    city = db.Column(db.String(64), index=True, nullable=True, comment="市")
    is_pc = db.Column(db.Boolean(), nullable=True, comment="是否电脑")
    device = db.Column(db.String(128), nullable=True, comment="移动设备名")
    os = db.Column(db.String(128), comment="系统")
    browser = db.Column(db.String(128), comment="浏览器")
    ua = db.Column(db.String(512), comment="UA")
    headers = db.Column(db.JSON(), comment="请求头")

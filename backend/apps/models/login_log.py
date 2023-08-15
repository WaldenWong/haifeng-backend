#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend.apps.models import Base, db


class LoginLog(Base):
    __tablename__ = "login_log"

    user_id = db.Column(db.BigInteger(), index=True)
    ip = db.Column(db.String(128), index=True)
    port = db.Column(db.Integer())
    country = db.Column(db.String(64), nullable=True)
    province = db.Column(db.String(64), nullable=True)
    city = db.Column(db.String(64), index=True, nullable=True)
    is_pc = db.Column(db.Boolean(), nullable=True)
    device = db.Column(db.String(128), nullable=True)
    os = db.Column(db.String(128))
    browser = db.Column(db.String(128))
    ua = db.Column(db.String(512))
    headers = db.Column(db.JSON())

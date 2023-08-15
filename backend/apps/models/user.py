#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from sqlalchemy import text

from backend.apps.models import Base, db
from backend.apps.settings import settings


def default_expired_at() -> datetime:
    return datetime.now() + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)


class User(Base):
    __tablename__ = "user"

    username = db.Column(db.String(32), index=True)
    password = db.Column(db.String(100))
    phone = db.Column(db.String(11), unique=True, nullable=True)
    real_name = db.Column(db.String(11), nullable=True)
    avatar = db.Column(db.String(256), nullable=True)  # 头像
    expired_at = db.Column(db.DateTime(), default=default_expired_at)
    stopped_on = db.Column(db.DateTime(), nullable=True)
    activated = db.Column(db.Boolean(), index=True, server_default=text("true"))
    creator = db.Column(db.BigInteger(), index=True, nullable=True)

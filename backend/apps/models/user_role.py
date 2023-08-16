#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend.apps.models import Base, db


class UserRole(Base):
    __tablename__ = "user_role"
    __table_args__ = {"comment": "用户权限"}

    role = db.Column(db.String(64), index=True, comment="父权限")
    user_id = db.Column(db.BigInteger(), index=True, comment="用户ID")
    show = db.Column(db.String(64), nullable=True, comment="子权限")

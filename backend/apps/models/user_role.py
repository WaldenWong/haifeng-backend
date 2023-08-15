#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend.apps.models import Base, db


class UserRole(Base):
    __tablename__ = "user_role"

    role = db.Column(db.String(64), index=True)
    user_id = db.Column(db.BigInteger(), index=True)
    show = db.Column(db.String(64), nullable=True)

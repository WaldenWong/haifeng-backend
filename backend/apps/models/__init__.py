#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    为了标识数据库模型，将所有调用的数据库模型名加上ORM后缀
    如：form . models.user import User as UserORM
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Type, Union

from gino import Gino
from pydantic import BaseModel, Json, create_model
from sqlalchemy.dialects.postgresql import JSONB, UUID

db = Gino()
db.JSONB, db.UUID = (JSONB, UUID)


class Base(db.Model):  # type: ignore
    __abstract__ = True
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    created_on = db.Column(db.DateTime, default=datetime.now, server_default=db.func.now(), index=True)
    updated_on = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now, server_default=db.func.now(), index=True
    )

    def to_dict(self) -> Dict[str, Union[str, None]]:
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    @classmethod
    async def get_by(cls, **kwargs: Any):  # type: ignore[no-untyped-def]
        sql = cls.query.with_for_update()
        for k, v in kwargs.items():
            sql = sql.where(getattr(cls, k) == v)
        return await sql.gino.first()

    @classmethod
    async def get_all(cls, **kwargs: Any):  # type: ignore[no-untyped-def]
        sql = cls.query.with_for_update()
        for k, v in kwargs.items():
            sql = sql.where(getattr(cls, k) == v)
        return await sql.gino.all()


def model_to_schema(db_model: Base) -> Type[BaseModel]:
    fields = {}
    for column in db_model.__table__.columns:
        python_type: Any
        name = str(column.name)
        if column.type.__visit_name__ == "UUID":
            python_type = uuid.UUID
        elif column.type.__visit_name__ in ["JSON", "JSONB"]:
            python_type = Json
        else:
            python_type = column.type.python_type
        assert python_type, f"Could not infer python_type for {column}"
        default = None
        if column.default is None and not column.nullable:
            default = ...
        fields[name] = (python_type, default)

    return create_model(db_model.__name__, **fields)  # type: ignore
